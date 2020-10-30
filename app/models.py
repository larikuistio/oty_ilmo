from app import db

class pubivisaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamname = db.Column(db.String(128))

    etunimi0 = db.Column(db.String(64))
    sukunimi0 = db.Column(db.String(64))
    phone0 = db.Column(db.String(32))
    email0 = db.Column(db.String(128))
    kilta0 = db.Column(db.String(16))

    etunimi1 = db.Column(db.String(64))
    sukunimi1 = db.Column(db.String(64))
    phone1 = db.Column(db.String(32))
    email1 = db.Column(db.String(128))
    kilta1 = db.Column(db.String(16))

    etunimi2 = db.Column(db.String(64))
    sukunimi2 = db.Column(db.String(64))
    phone2 = db.Column(db.String(32))
    email2 = db.Column(db.String(128))
    kilta2 = db.Column(db.String(16))

    etunimi3 = db.Column(db.String(64))
    sukunimi3 = db.Column(db.String(64))
    phone3 = db.Column(db.String(32))
    email3 = db.Column(db.String(128))
    kilta3 = db.Column(db.String(16))
    
    consent0 = db.Column(db.Boolean())
    consent1 = db.Column(db.Boolean())
    consent2 = db.Column(db.Boolean())

    datetime = db.Column(db.DateTime())

    personcount = db.Column(db.Integer())


class korttijalautapeliiltaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(128))
    
    kilta = db.Column(db.String(16))
    
    consent0 = db.Column(db.Boolean())
    consent1 = db.Column(db.Boolean())
    consent2 = db.Column(db.Boolean())
    
    datetime = db.Column(db.DateTime())


class fuksilauluiltaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    email = db.Column(db.String(128))
    
    consent1 = db.Column(db.Boolean())
    
    datetime = db.Column(db.DateTime())


class slumberpartyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column(db.String(64))
    sukunimi = db.Column(db.String(64))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(128))
    
    kilta = db.Column(db.String(16))
    
    consent0 = db.Column(db.Boolean())
    consent1 = db.Column(db.Boolean())
    consent2 = db.Column(db.Boolean())
    
    datetime = db.Column(db.DateTime())



class exitModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    aika = db.Column(db.String(16))
    huone = db.Column(db.String(128))

    etunimi0 = db.Column(db.String(64))
    sukunimi0 = db.Column(db.String(64))
    phone0 = db.Column(db.String(32))
    email0 = db.Column(db.String(128))

    etunimi1 = db.Column(db.String(64))
    sukunimi1 = db.Column(db.String(64))

    etunimi2 = db.Column(db.String(64))
    sukunimi2 = db.Column(db.String(64))

    etunimi3 = db.Column(db.String(64))
    sukunimi3 = db.Column(db.String(64))

    etunimi4 = db.Column(db.String(64))
    sukunimi4 = db.Column(db.String(64))

    etunimi5 = db.Column(db.String(64))
    sukunimi5 = db.Column(db.String(64))
    
    consent0 = db.Column(db.Boolean())

    datetime = db.Column(db.DateTime())