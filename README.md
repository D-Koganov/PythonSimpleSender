# PythonSimpleSender

1. Create virtual environment
python -m venv venv

-m venv venv -> use module venv to create virtual environment with name venv (can be any other)

2. Activate
Linux:
source venv/bin/activate
Windows:
venv\Scripts\activate.bat

3. Import dependencies
pip install -r requirements.txt

requirements.txt was created using "pip freeze > requirements.txt".
//In ubuntu "pkg_resources=0.0.0" - is a bug. Can remove

4. Play around

5. Deactivate
Linux:
deactivate
Windows:
venv\Scripts\deactivate.bat
