# oty_ilmo
Event registration forms for Oulun Teekkariyhdistys ry

## run development server
```shell
python3 -m venv env
pip install -r requirements
export FLASK_APP=app.py
flask run
```

## kapsi deployment

.htaccess
```apache
# http -> https
RewriteEngine On
RewriteCond %{ENV:HTTPS} !on
RewriteRule (.*) https://%{SERVER_NAME}%{REQUEST_URI} [R=301,L]


RewriteEngine On
RewriteRule ^$ http://lakka.n.kapsi.fi:62733/ [P]
RewriteRule ^(index\.html)$ http://lakka.n.kapsi.fi:62733/ [P]
RewriteRule ^(.*)$ http://lakka.n.kapsi.fi:62733/$1 [P]
```
starting gunicorn
```shell
gunicorn --workers=1 --worker-connections=400 --bind=0.0.0.0:62733 wsgi:app --name=ilmot --timeout 20
```
