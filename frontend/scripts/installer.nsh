!macro customInit
  DetailPrint "Terminating any active PRAHARI AI background processes..."
  nsExec::Exec 'taskkill /F /IM "PRAHARI AI.exe" /T'
  nsExec::Exec 'taskkill /F /IM "aegis_backend.exe" /T'
  nsExec::Exec 'taskkill /F /IM "electron.exe" /T'
  Sleep 800
!macroend

!macro customInstall
  DetailPrint "Ensuring clean destination files..."
  nsExec::Exec 'taskkill /F /IM "PRAHARI AI.exe" /T'
  nsExec::Exec 'taskkill /F /IM "aegis_backend.exe" /T'
!macroend

!macro customUnInit
  DetailPrint "Terminating any active PRAHARI AI background processes..."
  nsExec::Exec 'taskkill /F /IM "PRAHARI AI.exe" /T'
  nsExec::Exec 'taskkill /F /IM "aegis_backend.exe" /T'
  Sleep 800
!macroend
