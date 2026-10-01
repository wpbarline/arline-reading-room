$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
# Reading and narration run independently of the language model.
& "$root\Start-Server.ps1"
if(Test-Path "$root\installed-app.json") {
    $app=Get-Content "$root\installed-app.json" -Raw | ConvertFrom-Json
    Start-Process -FilePath $app.target -ArgumentList $app.arguments
} else {
    Start-Process -FilePath 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' -ArgumentList '--app=http://127.0.0.1:8765/'
}
