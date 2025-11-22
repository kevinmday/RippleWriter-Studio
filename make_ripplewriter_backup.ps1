# ============================================================
# RippleWriter Studio — Full Project Backup Script
# Creates a timestamped folder and copies the entire directory
# ============================================================

param(
    [string]$SourcePath = ".",
    [string]$BackupPrefix = "ripplewriter_backup"
)

# Timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFolder = "$BackupPrefix" + "_$timestamp"

# Create backup folder
New-Item -ItemType Directory -Path $backupFolder | Out-Null

# Copy all files & folders (recursive)
Copy-Item -Path "$SourcePath\*" -Destination $backupFolder -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "============================================================"
Write-Host "  RippleWriter Backup Completed"
Write-Host "  Location: $backupFolder"
Write-Host "  Timestamp: $timestamp"
Write-Host "============================================================"
