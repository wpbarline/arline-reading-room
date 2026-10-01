param([Parameter(Mandatory=$true)][string]$InputPath,[Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $voice.SelectVoice('Microsoft Zira Desktop')
    $voice.Rate = -1
    $voice.SetOutputToWaveFile($OutputPath)
    $text = [System.IO.File]::ReadAllText($InputPath, [System.Text.Encoding]::UTF8)
    $voice.Speak($text)
} finally { $voice.Dispose() }
