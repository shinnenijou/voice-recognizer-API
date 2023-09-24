; The name of the installer
Name "FenrirChan API ver"

; The file to write
OutFile "fenrir_chan_API_ver.exe"

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
SectionEnd ; end the section
