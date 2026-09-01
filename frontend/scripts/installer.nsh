!macro customHeader
  !define INSTALLER_KILL_APP
  !define UNINSTALLER_KILL_APP
!macroend

!macro TerminateProcesses
  DetailPrint "Ensuring all previous instances and background workers are terminated..."
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "PRAHARI AI.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "aegis_backend.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "electron.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "python.exe" 2>nul'
  nsExec::Exec 'cmd.exe /c taskkill /F /T /IM "uvicorn.exe" 2>nul'
  Sleep 500
!macroend

!macro customInit
  !insertmacro TerminateProcesses
!macroend

!macro customCheckAppRunning
  !insertmacro TerminateProcesses
!macroend

!macro customInstall
  !insertmacro TerminateProcesses
!macroend

!macro customUnInit
  !insertmacro TerminateProcesses
!macroend
