# Privilege, write and process search recipes

`git diff BASE...HEAD -U0 | grep '^+' > added.txt`; `rg -n PATTERN added.txt`. Read each hit in context.

## Language-agnostic

```bash
rg -n '\.(bashrc|zshrc|profile|bash_profile|zprofile|config/autostart)|\.ssh|authorized_keys|crontab|/etc/|LaunchAgents|LaunchDaemons|systemd|\.git/hooks|sudoers|registry|HKEY_|schtasks' added.txt
rg -n '0o?7[0-7][0-7]|chmod|umask|0o?666|0o?777|set_permissions|icacls' added.txt
rg -n '/tmp/|TMPDIR|mktemp|tmpnam|tempfile|temp_dir' added.txt
rg -n '(token|secret|password|api.?key|bearer)' -i added.txt | rg -i 'log|print|debug|format|eprintln|echo|url|argv|arg\('
```

## Rust

```bash
rg -n 'unsafe|extern "(C|system)"|transmute|from_raw|\*mut|\*const|MaybeUninit|libc::|windows(_sys)?::' added.txt
rg -n 'fs::(write|create_dir|remove|rename|copy|set_permissions)|File::create|OpenOptions|symlink|canonicalize|\.join\(' added.txt
rg -n 'Command::new|\.arg\(|\.args\(|\.env\(|sh -c|cmd /c' added.txt
rg -n 'TcpListener::bind|UnixListener|bind\(|0\.0\.0\.0|127\.0\.0\.1|localhost|Host:|Origin|Content-Length|set_read_timeout|set_nonblocking' added.txt
rg -n 'rand::|thread_rng|SystemTime.*(seed|token)|/dev/urandom|BCryptGenRandom|getrandom|OsRng' added.txt
rg -n 'bincode|serde_(json|yaml)|from_slice|deserialize|serde_pickle' added.txt
rg -n 'Content-Security-Policy|sandbox|allow-scripts|srcdoc|iframe|X-Frame-Options|frame-ancestors' added.txt
```
Check any `unsafe` for a `// SAFETY:` comment: `rg -n -B2 'unsafe' added.txt`.

## Python

```bash
rg -n 'open\(.*[\'"][wa]|shutil\.|os\.(rename|remove|chmod|makedirs|symlink)|Path\(.*\)\.(write|mkdir|unlink)|tarfile|zipfile|extractall' added.txt
rg -n 'subprocess|os\.system|os\.popen|shell=True|Popen|eval\(|exec\(|pickle|yaml\.load\(|marshal|shelve' added.txt
rg -n 'random\.|uuid\.uuid1|time\.time\(\).*token|secrets\.|os\.urandom' added.txt
rg -n 'http\.server|socketserver|Flask|FastAPI|uvicorn|bind|0\.0\.0\.0|app\.run' added.txt
```

## JavaScript / TypeScript

```bash
rg -n 'fs\.(write|append|mkdir|rm|rename|chmod|symlink)|createWriteStream|path\.join\(|path\.resolve\(' added.txt
rg -n 'child_process|exec(Sync)?\(|spawn(Sync)?\(|shell: *true|eval\(|new Function|vm\.run' added.txt
rg -n 'Math\.random|crypto\.randomBytes|crypto\.getRandomValues|randomUUID' added.txt
rg -n 'listen\(|0\.0\.0\.0|cors\(|Access-Control|innerHTML|dangerouslySetInnerHTML|postMessage|sandbox=' added.txt
rg -n 'JSON\.parse|yaml\.load|serialize|unserialize|deserialize' added.txt
```

## Go

```bash
rg -n 'os\.(Create|OpenFile|WriteFile|Mkdir|Remove|Rename|Chmod|Symlink)|ioutil\.Write|filepath\.(Join|Clean)|0o?[0-7]{3}' added.txt
rg -n 'exec\.Command|syscall\.|unsafe\.|cgo|import "C"' added.txt
rg -n 'math/rand|crypto/rand|ListenAndServe|net\.Listen|0\.0\.0\.0|InsecureSkipVerify|gob\.|yaml\.Unmarshal' added.txt
```

## Shell

```bash
rg -n '>>? *(~|\$HOME|/etc|/usr|/var)|tee |chmod|chown|sudo|ln -s|mktemp|rm -rf *\$|eval|\$\(.*\$[A-Za-z_]' added.txt
rg -n 'curl.*(token|key|secret)|echo .*(token|key|secret)|set -x' -i added.txt
```
Unquoted variables in `rm`, `cp`, `mv`, `cd` and missing `set -euo pipefail` are review items.

## Terminal escapes

```bash
rg -n '\\x1b|\\u001b|\\033|\\e\[|OSC|CSI|DCS' added.txt     # emitted sequences
```
Then trace whether any untrusted string reaches the same output path without control-character stripping.
