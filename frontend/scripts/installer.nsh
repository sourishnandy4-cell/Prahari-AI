!macro customHeader
  !define INSTALLER_KILL_APP
  !define UNINSTALLER_KILL_APP
!macroend

!macro TerminatePrahariProcessTree
  DetailPrint "Force-closing any running PRAHARI AI and backend processes..."
  
  # 1. Force kill all known executables and their child process trees
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "PRAHARI AI.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "aegis_backend.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "electron.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "python.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "uvicorn.exe" 2>nul'

  # 2. PowerShell deep search: force kill any process running inside $INSTDIR or matching app name
  nsExec::Exec 'powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "Get-Process -ErrorAction SilentlyContinue | Where-Object { ($$_.ProcessName -match ''prahari|aegis_backend|electron'') -or ($$_.Path -and $$_.Path -like ''*$INSTDIR*'' -and $$_.Id -ne $$PID) } | Stop-Process -Force -ErrorAction SilentlyContinue"'

  # 3. Direct nsProcess plugin kill
  ${nsProcess::KillProcess} "PRAHARI AI.exe" $0
  ${nsProcess::KillProcess} "aegis_backend.exe" $0
  ${nsProcess::KillProcess} "electron.exe" $0

  Sleep 800
!macroend

# Override electron-builder's checkAppRunning to avoid the "cannot be closed" retry dialog
!macro customCheckAppRunning
  !insertmacro TerminatePrahariProcessTree
  # Secondary sweep to ensure clean directory state
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "PRAHARI AI.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "aegis_backend.exe" 2>nul'
  Sleep 300
!macroend

!macro customInit
  !insertmacro TerminatePrahariProcessTree
!macroend

!macro customInstall
  DetailPrint "Preparing destination folder and unlocking files..."
  !insertmacro TerminatePrahariProcessTree
  # Remove read-only / system attributes from $INSTDIR to prevent CopyFiles failure
  nsExec::Exec 'cmd.exe /c attrib -R -S -H "$INSTDIR\*.*" /S /D 2>nul'
  # Remove existing main executable and backend to ensure fresh clean copy
  Delete "$INSTDIR\PRAHARI AI.exe"
  Delete "$INSTDIR\resources\backend\aegis_backend\aegis_backend.exe"
  Delete "$INSTDIR\resources\app.asar"
  Sleep 500
!macroend

!macro customUnInit
  !insertmacro TerminatePrahariProcessTree
!macroend


