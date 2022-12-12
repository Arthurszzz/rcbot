@echo off
color 0a
echo.
set /p a="Coloque o nome do seu EXE : "
if [%a%]==[] ( 
    CALL:error
    pause
    EXIT /B %ERRORLEVEL% 
) 
if [%a%] NEQ [] (
    CALL:main
    EXIT /B %ERRORLEVEL% 
)

:main
echo.
echo Nome e: %a% 
pip uninstall -y enum34
pyinstaller --onefile --clean --noconfirm --noconsole -n %a% -i NONE .\main.py
del /s /q /f %a%.spec
rmdir /s /q __pycache__
rmdir /s /q build
EXIT /B %ERRORLEVEL% 

:error
echo.
echo Bro coloca o nome do EXE
EXIT /B %ERRORLEVEL% 
