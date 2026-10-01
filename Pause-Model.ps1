$ErrorActionPreference='Stop'
$task=Get-ScheduledTask -TaskName BonsaiService -ErrorAction SilentlyContinue
$running=$task -and $task.State -eq 'Running'
if($running) {
    Stop-ScheduledTask -TaskName BonsaiService
    Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'llama-server.exe' -and $_.CommandLine -like '*C:\models\Qwen3.5-2B-Q4_K_M.gguf*' } | ForEach-Object { & taskkill.exe /PID $_.ProcessId /F 2>$null | Out-Null }
}
@{resume=[bool]$running} | ConvertTo-Json -Compress
