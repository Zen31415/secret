# secret
Flask web app for sending secure messages.

## Bootstrapping
```
cd to project folder
sudo apt install python3-pip sqlite3 python3.10-venv docker docker-compose
python3 -m venv venv
. venv/bin/activate
pip install flask
pip install -r requirements.txt
ctrl+shift+p -> python: select interpreter

FLASK_APP=app.py FLASK_DEBUG=development python app.py

once the project is installable: pip install -e .

sudo docker-compose up
flask --app flaskr init-db ## (or just flask init-db)
flask --app flaskr --debug run

git clone <url>
git status
git commit
git push -u origin main
```
