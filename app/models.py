from app import db

class sitsiModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    email = db.Column(db.String(128))
    alkoholi = db.Column(db.String(32))
    mieto = db.Column(db.String(32))
    pitsa = db.Column(db.String(32))
    allergiat = db.Column(db.String(256))
    consent0 = db.Column(db.Boolean())
    consent1 = db.Column(db.Boolean())
    datetime = db.Column(db.DateTime())


class fucuModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    email = db.Column(db.String(128))
    puh = db.Column(db.String(32))
    lahtopaikka = db.Column(db.String(32))
    kiintio = db.Column(db.String(32))
    consent0 = db.Column(db.Boolean())
    consent1 = db.Column(db.Boolean())
    datetime = db.Column(db.DateTime())