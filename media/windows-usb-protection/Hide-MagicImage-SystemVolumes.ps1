# Remove the Windows access paths of the USB medium's boot volumes.
# No partition attributes, files or filesystem metadata are changed.
$ErrorActionPreference = 'Stop'
$logDirectory = 'C:\Windows\Addins'
New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
$logPath = Join-Path $logDirectory 'MagicImage-USB-VolumeGuard.log'

function Write-GuardLog([string]$message) {
    Add-Content -LiteralPath $logPath -Encoding UTF8 -Value ('[{0}] {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $message)
}

try {
    Write-GuardLog 'START: Boot volumes are removed from this Windows session only.'
    # Split-Path returns e.g. "G:\\". Take the drive letter directly.
    $repositoryDrive = (Split-Path -Qualifier $PSScriptRoot).Substring(0, 1)
    $repositoryPartition = Get-Partition -DriveLetter $repositoryDrive -ErrorAction Stop
    $repositoryVolume = Get-Volume -DriveLetter $repositoryDrive -ErrorAction Stop
    if ($repositoryVolume.FileSystemLabel -ne 'MISOLOIMAGES') {
        throw "Script was not started from MISOLOIMAGES (found: $($repositoryVolume.FileSystemLabel))."
    }
    $repositoryDisk = $repositoryPartition.DiskNumber
    Write-GuardLog "Repository confirmed: disk $repositoryDisk, partition $($repositoryPartition.PartitionNumber), drive ${repositoryDrive}: ."

    foreach ($label in 'MISODEBIAN', 'ACRONIS', 'MISOLOBOOT') {
        $volume = Get-Volume -FileSystemLabel $label -ErrorAction SilentlyContinue | Where-Object { $_.DriveLetter } | Where-Object {
            try { (Get-Partition -DriveLetter $_.DriveLetter -ErrorAction Stop).DiskNumber -eq $repositoryDisk } catch { $false }
        } | Select-Object -First 1
        if (-not $volume) {
            Write-GuardLog "${label}: no drive letter present."
            continue
        }
        $letter = [string]$volume.DriveLetter
        $partition = Get-Partition -DriveLetter $letter -ErrorAction Stop
        if ($partition.DiskNumber -ne $repositoryDisk) {
            throw "${label}: belongs to unexpected disk $($partition.DiskNumber), expected $repositoryDisk."
        }
        Remove-PartitionAccessPath -DiskNumber $partition.DiskNumber -PartitionNumber $partition.PartitionNumber -AccessPath ("{0}:\\" -f $letter) -ErrorAction Stop
        Write-GuardLog "${label}: removed ${letter}: from disk $($partition.DiskNumber), partition $($partition.PartitionNumber)."
    }
    Write-GuardLog "MISOLOIMAGES remains available as ${repositoryDrive}: ."
    Write-GuardLog 'END: success.'
}
catch {
    Write-GuardLog ('ERROR: ' + $_.Exception.Message)
    exit 1
}
