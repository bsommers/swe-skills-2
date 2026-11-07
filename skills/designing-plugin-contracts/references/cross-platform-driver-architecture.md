# Cross-Platform Driver Architecture (Windows, macOS, Linux)

Build driver boundaries so **Windows, macOS, and Linux** are first-class targets from day one. Keep host/core code 100% OS-agnostic and encapsulate all platform differences inside driver implementations that share one contract test suite.

---

## 1. Tri-OS Seam Matrix

| Subsystem Seam | Windows (`win32` / `#[cfg(windows)]`) | macOS (`darwin` / `#[cfg(target_os = "macos")]`) | Linux (`linux` / `#[cfg(target_os = "linux")]`) | Contract Normalization Rule |
|---|---|---|---|---|
| **Terminal / PTY** | **ConPTY** (`CreatePseudoConsole`, `ResizePseudoConsole`, `ClosePseudoConsole`) | **POSIX PTY** (`openpty` / `forkpty`, `ioctl(TIOCSWINSZ)`, `SIGWINCH`) | **POSIX PTY** (`openpty` / `forkpty`, `/dev/ptmx`, `ioctl(TIOCSWINSZ)`) | Expose `spawn()`, `write()`, `resize(cols, rows)`, `close()` with UTF-8 stream framing. |
| **Process Tree & Kill** | **Job Objects** (`CreateJobObject`, `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`) + `TerminateProcess` | Process group (`setpgid`, `killpg` / `kill(-pgid, SIGTERM)` then `SIGKILL`) | Process group (`setpgid`, `kill(-pgid, SIGTERM)`) or `PR_SET_PDEATHSIG` / cgroups | Driver `close()` terminates the entire descendant tree deterministically and resolves `onExit(code)`. |
| **Executable Lookup** | `PATH` + `PATHEXT` (`.exe`, `.cmd`, `.bat`, `.ps1`); `cmd.exe /c` for batch shims | `PATH` + `chmod +x` executable mode bit; `/bin/zsh` or `/bin/bash` (Bash 3.2 default) | `PATH` + `chmod +x` executable mode bit; `/bin/sh` or `/usr/bin/env bash` | Driver resolves binary via cross-platform `which` helper; always pass argv arrays (never raw shell strings). |
| **Local IPC Transport** | **Named Pipes** (`\\.\pipe\<app>-<id>`) or authenticated `127.0.0.1` loopback TCP | **Unix domain socket** in `$TMPDIR` (must keep path **< 104 bytes** for `sun_path`) | **Unix domain socket** in `${XDG_RUNTIME_DIR:-/tmp}` (`0600` perms, `< 108` bytes) | Expose uniform `TransportStream` (`connect`, `listen`, `send`, `recv`, `close`). |
| **Filesystem & Atomic Write** | `MoveFileExW(..., MOVEFILE_REPLACE_EXISTING)`; open files lock deletion/rename; `\` & UNC `\\?\` | APFS (case-insensitive by default); `rename(2)` atomic; `FSEvents` watcher | ext4/xfs (case-sensitive); `rename(2)` atomic; `inotify` watcher | Use `Path`/`PathBuf`; close file handles before atomic temp-file rename; normalize `CRLF`/`LF` on text I/O. |
| **Standard Directories** | Config: `%APPDATA%\<app>` · Cache/State: `%LOCALAPPDATA%\<app>` | Config: `~/Library/Application Support/<app>` · Cache: `~/Library/Caches/<app>` | Config: `${XDG_CONFIG_HOME:-~/.config}/<app>` · State: `${XDG_STATE_HOME:-~/.local/state}/<app>` | Provide a single `AppPaths` provider injected into drivers (`designing-testable-seams`). |
| **Signals & Shutdown** | `SetConsoleCtrlHandler` (`CTRL_C_EVENT`, `CTRL_BREAK_EVENT`, `CTRL_CLOSE_EVENT`) | `sigaction` (`SIGINT`, `SIGTERM`, `SIGHUP`, `SIGCHLD`) | `sigaction` / `signalfd` (`SIGINT`, `SIGTERM`, `SIGHUP`, `SIGCHLD`) | Translate OS signals into a single host `ShutdownToken` / `onShutdown` event. |

---

## 2. Driver Registration & Factory Pattern

Never write `if sys.platform == "win32":` inside business logic. Resolve the platform driver once at composition root:

```python
def create_default_session_driver(os_name: str = sys.platform, syscall_seam=None) -> SessionDriver:
    if os_name.startswith("win"):
        return WindowsConPtyDriver(seam=syscall_seam or Win32ConPtySeam())
    if os_name == "darwin":
        return MacOSPosixPtyDriver(seam=syscall_seam or PosixPtySeam())
    if os_name.startswith("linux"):
        return LinuxPosixPtyDriver(seam=syscall_seam or PosixPtySeam())
    raise UnsupportedPlatformError(f"Unsupported platform: {os_name}")
```

---

## 3. Testing & Coverage Across All Three OSes

1. **Injected Low-Level Seams for Cross-Host Unit Coverage:**
   Separate each OS driver into:
   - **Driver state/protocol logic** (e.g., `WindowsConPtyDriver`, `MacOSPosixPtyDriver`, `LinuxPosixPtyDriver`) that takes a thin syscall/transport seam (`Win32ConPtySeam`, `PosixPtySeam`), and
   - **Thin native syscall bindings.**
   This allows unit tests for `WindowsConPtyDriver`, `MacOSPosixPtyDriver`, and `LinuxPosixPtyDriver` to run and achieve **>90% branch coverage on any host OS** using fake syscall seams.
2. **Parameterized Contract Test Suite:**
   Run the exact same contract test suite against `[MockDriver, NativeHostDriver]`:
   - Spawn & UTF-8 streaming output
   - Window/buffer resize propagation
   - Non-zero exit code & error normalization
   - Child process-tree cleanup on `close()` (no orphan processes)
   - Path handling with spaces, Unicode, and long paths
3. **Tri-OS CI Verification Matrix (`windows-latest`, `macos-latest`, `ubuntu-latest`):**
   Execute native integration/system tiers and collect coverage on all three OSes (`test-coverage`), merging or asserting per-OS coverage floors so no OS driver regresses.
