# oty_ilmo
Event registration forms for Oulun Teekkariyhdistys ry


## kapsi

.htaccess
```
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
```
gunicorn -w 2 -t 2 --worker-connections=200 --bind=0.0.0.0:62733 wsgi:app --name=ilmot --timeout 60 --daemon
```
