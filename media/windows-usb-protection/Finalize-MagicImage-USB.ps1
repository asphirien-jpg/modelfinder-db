param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Za-z]$')]
    [string]$SourceDrive,
    [ValidateRange(1, 30)]
    [int]$DelaySeconds = 4
)

$ErrorActionPreference = 'Stop'
$logDirectory = 'C:\Windows\Addins'
New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
$logPath = Join-Path $logDirectory 'MagicImage-USB-Finalize.log'

function Write-FinalizeLog([string]$message) {
    Add-Content -LiteralPath $logPath -Encoding UTF8 -Value ('[{0}] {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $message)
}

try {
    Start-Sleep -Seconds $DelaySeconds
    $volume = Get-Volume -DriveLetter $SourceDrive -ErrorAction Stop
    if ($volume.FileSystemLabel -ne 'MISOLOIMAGES') {
        throw "Safety check failed: ${SourceDrive}: is '$($volume.FileSystemLabel)', not MISOLOIMAGES."
    }
    Write-FinalizeLog "Finalizing ${SourceDrive}: / MISOLOIMAGES."
    $mountPath = ('{0}:\\' -f $SourceDrive)
    & "$env:SystemRoot\System32\mountvol.exe" $mountPath '/p'
    if ($LASTEXITCODE -ne 0) {
        throw "mountvol /p failed for $mountPath (exit code $LASTEXITCODE)."
    }
    Write-FinalizeLog 'USB data volume was dismounted successfully.'
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show(
        "Installation vollstaendig abgeschlossen.`r`nDie USB-SSD wurde sicher getrennt. Sie kann jetzt abgezogen werden.`r`n`r`nInstalace byla uspesne dokoncena.`r`nUSB SSD byla bezpecne odpojena. Nyni ji muzete odpojit.",
        'Magic Image - USB-SSD kann entfernt werden',
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
    exit 0
}
catch {
    Write-FinalizeLog ('FINALIZE ERROR: ' + $_.Exception.Message)
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show(
        "Installation ist fertig, aber die USB-SSD konnte nicht sicher getrennt werden.`r`nBitte nicht sofort abziehen.`r`n`r`nInstalace je dokoncena, ale USB SSD nelze bezpecne odpojit.`r`nNeodpojujte ji ihned.",
        'Magic Image - USB-SSD noch angeschlossen lassen',
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Warning
    ) | Out-Null
    exit 1
}
