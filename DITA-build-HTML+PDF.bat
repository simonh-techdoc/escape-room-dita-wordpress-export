@echo off

REM ===== PORTABLE JAVA =====
set "JAVA_HOME=C:\DITA\java25"
set "PATH=%JAVA_HOME%\bin;%PATH%"

REM ===== DITA-OT =====
set "DITA_OT_DIR=C:\DITA\dita-ot-4.4"

REM ===== PROJEKT =====
set "PROJECT_DIR=%~dp0"
set "MAP_FILE=%PROJECT_DIR%maps\main.ditamap"

REM ===== OUTPUT =====
set "OUT_ROOT=%PROJECT_DIR%output-html"
set "OUT_HTML=%OUT_ROOT%"
set "OUT_PDF=%PROJECT_DIR%output-pdf"

echo ===== DEBUG =====
echo PROJECT_DIR: %PROJECT_DIR%
echo MAP_FILE: %MAP_FILE%
echo DITA_OT_DIR: %DITA_OT_DIR%
echo.

pause

REM ===== CHECK =====
if not exist "%MAP_FILE%" (
  echo FEHLER: main.ditamap nicht gefunden!
  pause
  exit
)

REM ===== ORDNER =====
if not exist "%OUT_HTML%" mkdir "%OUT_HTML%"
if not exist "%OUT_PDF%" mkdir "%OUT_PDF%"

echo.
echo ===== BUILD HTML =====
call "%DITA_OT_DIR%\bin\dita.bat" -i "%MAP_FILE%" -f html5 -o "%OUT_HTML%" --processing-mode=lax --logfile="%OUT_HTML%\build.log"

echo.
echo ===== FIX HTML LINKS =====
powershell -Command "(Get-Content '%OUT_HTML%\index.html') -replace '../topics/', 'topics/' | Set-Content '%OUT_HTML%\index.html'"

echo.
echo ===== BUILD PDF =====
call "%DITA_OT_DIR%\bin\dita.bat" -i "%MAP_FILE%" -f pdf -o "%OUT_PDF%" --processing-mode=lax --logfile="%OUT_PDF%\build.log"

echo.
echo ===== OPEN OUTPUT =====
start "" "%OUT_HTML%\index.html"
start "" "%OUT_PDF%\main.pdf"

echo.
echo ===== FERTIG =====

pause
