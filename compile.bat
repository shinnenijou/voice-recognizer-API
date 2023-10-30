cd %~dp0\others\starter
call .\venv\Scripts\activate.bat
if exist starter.spec (del starter.spec)
if exist build (rd /s /q build)
if exist dist (rd /s /q dist)
pyinstaller -i="icon.ico" -w -D starter.py --name starter

cd %~dp0
if exist starter (rd /s /q starter)
mkdir starter
copy others\starter\dist\starter starter

"%ProgramFiles(x86)%\NSIS\makensis.exe" make-wizard.nsi

mkdir build
copy fenrir_chan.exe build\fenrir_chan.exe
del fenrir_chan.exe 

pause