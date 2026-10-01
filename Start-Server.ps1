$ErrorActionPreference='Stop'
$root=$PSScriptRoot
try { Invoke-RestMethod 'http://127.0.0.1:8765/api/status' -TimeoutSec 2 | Out-Null; return }
catch {}
Start-Process -FilePath "$root\runtime\python\python.exe" -ArgumentList "`"$root\assistant.py`"" -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput "$root\results\interface.log" -RedirectStandardError "$root\results\interface-errors.log"
for($attempt=0;$attempt -lt 30;$attempt++) {
    try { Invoke-RestMethod 'http://127.0.0.1:8765/api/status' -TimeoutSec 1 | Out-Null; return }
    catch { Start-Sleep -Milliseconds 500 }
}
throw 'The local reading service did not start. Check results/interface-errors.log.'
