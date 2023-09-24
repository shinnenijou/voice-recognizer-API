; The name of the installer
Name "FenrirChan"

; The file to write
OutFile "fenrir_chan.exe"

; Build Unicode installer
Unicode True

; The default installation directory
InstallDir $APPDATA\FenrirChan

;Request application privileges for Windows Vista
RequestExecutionLevel user
;--------------------------------
; Pages

Page directory
Page instfiles

;--------------------------------
; The stuff to install
Section "" ;No components page, name is not important
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  ; Put file there
  ;File HelloLiam.exe ;add a file.
  File /r "res" 
  File /r "starter"
  File /r "env"
  File "main.py"
  File "myPath.py"
  File "version.json"
  
  CreateShortCut "$DESKTOP\FenrirChan.lnk" "$INSTDIR\starter\starter.exe" "" "$INSTDIR\res\img\icon.ico" "0" "SW_SHOWNORMAL"
SectionEnd ; end the section
