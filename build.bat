set ROOT_DIR=%~dp0
echo %ROOT_DIR%

python -m venv venv & venv\Scripts\python -m pip install -r requirements.txt
venv/Scripts/activate & pyinstaller main.spec
python backend/build.py
