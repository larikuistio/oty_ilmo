from app import db

class pubivisaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(128))
    
    kilta = db.Column(db.String(16))
    
    consent0 = db.Column(db.Boolean())
    consent1 = db.Column(db.Boolean())

    datetime = db.Column(db.DateTime())


class korttijalautapeliiltaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(128))
    
    kilta = db.Column(db.String(16))
    
    consent0 = db.Column(db.Boolean())
    consent1 = db.Column(db.Boolean())
    
    datetime = db.Column(db.DateTime())


class korttijalautapeliiltaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    email = db.Column(db.String(128))
    
    consent0 = db.Column(db.Boolean())
    consent1 = db.Column(db.Boolean())
    
    datetime = db.Column(db.DateTime())