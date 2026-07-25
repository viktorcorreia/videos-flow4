# Gera locução via ElevenLabs.
# Uso: pwsh gen_tts.ps1 -Texto "..." -Saida locucao.mp3 [-Voice <id|apelido>] [-Model eleven_v3]
# Apelidos: achadinhos (padrão), maya-clean, maya-clone2, roberta, keren
param(
    [Parameter(Mandatory = $true)][string]$Texto,
    [Parameter(Mandatory = $true)][string]$Saida,
    [string]$Voice = 'achadinhos',
    [string]$Model = 'eleven_v3',
    [double]$Stability = 0.5
)
$ErrorActionPreference = 'Stop'

$apelidos = @{
    'achadinhos'  = 'eCG3FOlagpQysp74j2dG'  # Achadinhos Empolgada (oficial)
    'maya-clean'  = 'ph1QLaDEB0uoYVk3JlyM'  # Maya_Clean_v2
    'maya-clone2' = 'ZfzOjHm1eofljX1NATrx'  # Maya-Clone-v2 (pt-BR)
    'roberta'     = 'RGymW84CSmfVugnA5tvA'  # premade pt-BR
    'keren'       = '33B4UnXyTNbgLmdEDh5P'  # premade pt-BR
}
$voiceId = if ($apelidos.ContainsKey($Voice)) { $apelidos[$Voice] } else { $Voice }

$key = ((Get-Content 'C:\dev\tiktok-ugc-pipeline\.env' | Where-Object { $_ -match '^ELEVENLABS_API_KEY=' }) -replace '^ELEVENLABS_API_KEY=', '').Trim()
if (-not $key) { throw 'ELEVENLABS_API_KEY ausente' }

$body = @{
    text           = $Texto
    model_id       = $Model
    voice_settings = @{ stability = $Stability; similarity_boost = 0.75 }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Method Post -Uri "https://api.elevenlabs.io/v1/text-to-speech/$voiceId`?output_format=mp3_44100_128" `
    -Headers @{ 'xi-api-key' = $key } -ContentType 'application/json' -Body $body -OutFile $Saida

$dur = ffprobe -v error -show_entries format=duration -of csv=p=0 $Saida
Write-Host "OK: $Saida ($([math]::Round([double]$dur,2))s) voz=$Voice modelo=$Model"
