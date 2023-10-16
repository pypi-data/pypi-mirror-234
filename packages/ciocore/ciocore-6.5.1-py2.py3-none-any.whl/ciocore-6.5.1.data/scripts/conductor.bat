@echo off

echo Looking for Python...

WHERE python.exe
if ERRORLEVEL 1 (  
    echo WARNING: python.exe not found.
    echo Please find or install Python and add it to your Path variable. Then run this command again.
    echo If you don't want to add python to your Path, then you can use the full path to a Python installation.
    echo Example: "C:\some\tools\python\python.exe" "%~dp0conductor %*
    exit /b
)
python.exe "%~dp0\conductor" %*
