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

  # Clear any stale uninstaller registry keys that cause Error 2
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\34c77fc9-ccd4-532a-8513-a765c7133758"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\com.mrpl.prahari"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\34c77fc9-ccd4-532a-8513-a765c7133758"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\com.mrpl.prahari"
  DeleteRegKey HKLM "Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\34c77fc9-ccd4-532a-8513-a765c7133758"
  DeleteRegKey HKLM "Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\com.mrpl.prahari"

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
