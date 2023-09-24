cd %~dp0
call .\venv\Scripts\activate.bat
if exist starter.spec (del starter.spec)
if exist build (rd /s /q build)
if exist dist (rd /s /q dist)
pyinstaller -i="icon.ico" -w -D starter.py --name starter

if exist ..\..\starter (rd /s /q ..\..\starter)
mkdir ..\..\starter
copy dist\starter ..\..\starter
pause