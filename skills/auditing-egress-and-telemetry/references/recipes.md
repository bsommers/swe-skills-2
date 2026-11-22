# Egress and telemetry search recipes

Run over added lines: `git diff BASE...HEAD -U0 | grep '^+' > added.txt`, then `rg -n PATTERN added.txt`. Patterns are starting points; read each hit in context. For a whole tree, drop `added.txt` and search the tree.

## Language-agnostic

```bash
rg -n 'https?://|wss?://|ftp://' added.txt                 # literal URLs
rg -n '\b(sentry|datadog|segment|mixpanel|amplitude|posthog|rudderstack|bugsnag|rollbar|newrelic|honeycomb|opentelemetry|otlp|statsd|telemetry|analytics|beacon|phone.?home|crash.?report)\b' -i added.txt
rg -n '(machine.?id|hostname|whoami|getuid|USER(NAME)?|HOME|uname|os\.release|fingerprint|mac.?addr|/etc/machine-id|IOPlatformUUID)' -i added.txt
rg -n '(base64|btoa|hex).*(env|passwd|token|key|secret|cookie)' -i added.txt
rg -n '(update|version).?check|check.?for.?update|latest.?release|api\.github\.com' -i added.txt
```

## Rust

```bash
rg -n 'reqwest|ureq|hyper|isahc|surf|attohttpc|curl::|TcpStream::connect|UdpSocket|ToSocketAddrs|lookup_host|tokio::net|tungstenite|websocket|std::net' added.txt
rg -n 'Command::new\("(curl|wget|nc|ncat|powershell|ssh|scp)"' added.txt
rg -n 'build\.rs|\[build-dependencies\]|proc-macro|cargo:rustc-env' added.txt   # build-time code
rg -n 'xdg-open|open::that|webbrowser' added.txt
```
Check `Cargo.toml`/`Cargo.lock`: new `[dependencies]`, `git =`, `path =`, `registry =`, `[patch]`, changed `checksum`.

## Python

```bash
rg -n 'requests\.|urllib|http\.client|httpx|aiohttp|socket\.|smtplib|ftplib|websockets?|dns\.resolver|getaddrinfo|gethostbyname|webbrowser' added.txt
rg -n 'subprocess.*(curl|wget)|os\.system|exec\(|eval\(|__import__|pickle\.loads' added.txt
rg -n 'setup\.py|cmdclass|install_requires|entry_points|\.pth\b|sitecustomize' added.txt
```

## JavaScript / TypeScript

```bash
rg -n 'fetch\(|XMLHttpRequest|axios|got\(|node-fetch|undici|WebSocket|EventSource|sendBeacon|navigator\.|new Image\(\)\.src|net\.connect|dns\.|https?\.request' added.txt
rg -n '"(pre|post)?install"|"prepare"|"postinstall"|child_process|execSync|spawn\(' added.txt package.json
rg -n 'process\.env|os\.(hostname|userInfo|networkInterfaces)' added.txt
rg -n '<script src=|<link [^>]*href=|<iframe|@import|url\(' added.txt          # browser-side egress in HTML strings
```
Lockfile: `resolved` hosts other than the usual registry, `integrity` changes without a version change.

## Go

```bash
rg -n 'net/http|http\.(Get|Post|NewRequest|Client)|net\.(Dial|Lookup)|websocket|grpc\.Dial|smtp\.|os/exec|exec\.Command' added.txt
rg -n 'go:generate|//go:embed|replace .*=>|^require ' added.txt go.mod go.sum
```

## Shell

```bash
rg -n 'curl|wget|nc |ncat|/dev/tcp/|scp |rsync .*:|ssh |openssl s_client|dig |nslookup|host ' added.txt
rg -n '\| *(ba)?sh\b|eval|source <\(|base64 -d' added.txt
```

## CI and containers

```bash
rg -n 'pull_request_target|workflow_run|secrets\.|curl .*\|.*sh|uses: [^@]+@(main|master|v[0-9]+)$' added.txt .github
rg -n '^(FROM|RUN|ADD) .*(http|curl|wget)|ADD https?://' added.txt
```
