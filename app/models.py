from app import db

class sitsiModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    email = db.Column(db.String(128))
    holi = db.Column(db.String(32))
    mieto = db.Column(db.String(32))
    vakeva = db.Column(db.String(32))
    viini = db.Column(db.String(32))
    consent0 = db.Column(db.BooleanField())
    consent1 = db.Column(db.BooleanField())


