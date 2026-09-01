!macro customHeader
  !define INSTALLER_KILL_APP
  !define UNINSTALLER_KILL_APP
!macroend

!macro customInit
  DetailPrint "Terminating any active PRAHARI AI and backend processes..."
  nsExec::Exec 'cmd.exe /c taskkill /F /IM "PRAHARI AI.exe" /T'
  nsExec::Exec 'cmd.exe /c taskkill /F /IM "aegis_backend.exe" /T'
  nsExec::Exec 'cmd.exe /c taskkill /F /IM "electron.exe" /T'
  ${nsProcess::KillProcess} "PRAHARI AI.exe" $0
  ${nsProcess::KillProcess} "aegis_backend.exe" $0
  Sleep 1000
!macroend

!macro customInstall
  DetailPrint "Ensuring clean destination files..."
  nsExec::Exec 'cmd.exe /c taskkill /F /IM "PRAHARI AI.exe" /T'
  nsExec::Exec 'cmd.exe /c taskkill /F /IM "aegis_backend.exe" /T'
  ${nsProcess::KillProcess} "PRAHARI AI.exe" $0
  ${nsProcess::KillProcess} "aegis_backend.exe" $0
!macroend

!macro customUnInit
  DetailPrint "Terminating any active PRAHARI AI and backend processes..."
  nsExec::Exec 'cmd.exe /c taskkill /F /IM "PRAHARI AI.exe" /T'
  nsExec::Exec 'cmd.exe /c taskkill /F /IM "aegis_backend.exe" /T'
  ${nsProcess::KillProcess} "PRAHARI AI.exe" $0
  ${nsProcess::KillProcess} "aegis_backend.exe" $0
  Sleep 800
!macroend
