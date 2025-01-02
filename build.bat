set ROOT_DIR=%~dp0
echo %ROOT_DIR%

venv\Scripts\activate & python backend\build.py

pause