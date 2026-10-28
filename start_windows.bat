@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  set "PYTHON=py -3"
) else (
  set "PYTHON=python"
)
if not exist ".venv\Scripts\python.exe" (
  echo Tao moi moi truong Python...
  %PYTHON% -m venv .venv
  if errorlevel 1 goto :error
)
echo Cai dat thu vien can thiet...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m streamlit run app.py
exit /b 0
:error
echo Co loi xay ra. Kiem tra Python 3.10+ va ket noi Internet, sau do thu lai.
pause
exit /b 1
