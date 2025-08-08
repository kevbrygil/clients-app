set -e
pip3 install --upgrade pip
pip3 install psycopg2 pipenv
pipenv install --skip-lock --system --dev
python3 db_script.py
#gunicorn -b 0.0.0.0:5000 main:app
#gunicorn --reload --workers 1 --bind 0.0.0.0:5000 main:app
