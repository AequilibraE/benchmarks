$ErrorActionPreference = "Stop"

# 7-Zip installation check
if (-not (Get-Command "C:\Program Files\7-Zip\7z.exe" -ErrorAction SilentlyContinue)) {
  Write-Host "7-Zip is not installed. Installing..."
  Invoke-WebRequest -Uri https://www.7-zip.org/a/7z2201-x64.exe -OutFile 7z-installer.exe
  Start-Process -FilePath ".\7z-installer.exe" -ArgumentList "/S" -Wait
  Remove-Item -Path .\7z-installer.exe
} else {
  Write-Host "7-Zip is already installed."
}

# SpatiaLite installation check
if (-not (Test-Path "C:\spatialite\mod_spatialite.dll")) {
  Write-Host "SpatiaLite is not installed. Installing..."
  Invoke-WebRequest -Uri http://www.gaia-gis.it/gaia-sins/windows-bin-amd64/mod_spatialite-5.1.0-win-amd64.7z -OutFile mod_spatialite.7z
  & "C:\Program Files\7-Zip\7z.exe" x mod_spatialite.7z -oC:\spatialite
  Remove-Item -Path .\mod_spatialite.7z
  [Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";C:\spatialite", [System.EnvironmentVariableTarget]::Machine)
} else {
  Write-Host "SpatiaLite is already installed."
}

# UV installation check
$UV_VERSION = "0.6.5"
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
  Write-Host "UV is not installed. Installing..."
  Invoke-WebRequest -Uri https://astral.sh/uv/$UV_VERSION/install.ps1 -OutFile C:\TEMP\uv-install.ps1
  powershell -ExecutionPolicy Bypass -File C:\TEMP\uv-install.ps1
} else {
  Write-Host "UV is already installed."
}
