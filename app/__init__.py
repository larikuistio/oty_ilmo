from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config
from flask_wtf.csrf import CSRFProtect, CSRFError

csrf = CSRFProtect()

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models

db.create_all()
db.session.commit()

if __name__ == "__main__":
    app.run(debug = True)