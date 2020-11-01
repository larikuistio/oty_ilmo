from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional, length, Required, InputRequired, Optional


class RequiredIf(InputRequired):
    """Validator which makes a field required if another field is set and has a truthy value.
    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
        - https://www.reddit.com/r/flask/comments/7y1k6p/af_wtforms_required_if_validator/
    """

    field_flags = ('requiredif',)

    def __init__(self, other_field_name, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.message = message

    def __call__(self, form, field):
        other_field = form[self.other_field_name]
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)
        else:
            Optional().__call__(form, field)

class RequiredIfValue(InputRequired):
    """Validator which makes a field required if another field is set and has a truthy value.
    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
        - https://www.reddit.com/r/flask/comments/7y1k6p/af_wtforms_required_if_validator/
    """

    field_flags = ('requiredif',)

    def __init__(self, other_field_name, value, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.message = message
        self.value = value

    def __call__(self, form, field):
        other_field = form[self.other_field_name]
        value = self.value
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data == value):
            super(RequiredIfValue, self).__call__(form, field)
        else:
            Optional().__call__(form, field)




class pubivisaForm(FlaskForm):
    teamname = StringField('Joukkueen nimi *', validators=[DataRequired(), length(max=100)])

    etunimi0 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi0 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    phone0 = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
    email0 = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    kilta0 = SelectField('Kilta *', 
        choices=(['OTiT', 'OTiT'], ['SIK', 'SIK'], ['YMP', 'YMP'], ['KONE', 'KONE'], 
        ['PROSE', 'PROSE'], ['OPTIEM', 'OPTIEM'], ['ARK', 'ARK']), 
        validators=[DataRequired()])

    etunimi1 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi1 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    phone1 = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
    email1 = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    kilta1 = SelectField('Kilta *', 
        choices=(['OTiT', 'OTiT'], ['SIK', 'SIK'], ['YMP', 'YMP'], ['KONE', 'KONE'], 
        ['PROSE', 'PROSE'], ['OPTIEM', 'OPTIEM'], ['ARK', 'ARK']), 
        validators=[DataRequired()])

    etunimi2 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi2 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    phone2 = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
    email2 = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    kilta2 = SelectField('Kilta *', 
        choices=(['OTiT', 'OTiT'], ['SIK', 'SIK'], ['YMP', 'YMP'], ['KONE', 'KONE'], 
        ['PROSE', 'PROSE'], ['OPTIEM', 'OPTIEM'], ['ARK', 'ARK']), 
        validators=[DataRequired()])

    etunimi3 = StringField('Etunimi', validators=[length(max=50)])
    sukunimi3 = StringField('Sukunimi', validators=[length(max=50)])
    phone3 = StringField('Puhelinnumero', validators=[length(max=20)])
    email3 = StringField('Sähköposti', validators=[length(max=100)])
    kilta3 = SelectField('Kilta', 
        choices=(['OTiT', 'OTiT'], ['SIK', 'SIK'], ['YMP', 'YMP'], ['KONE', 'KONE'], 
        ['PROSE', 'PROSE'], ['OPTIEM', 'OPTIEM'], ['ARK', 'ARK']))

    consent0 = BooleanField('Sallin joukkueen nimen julkaisemisen osallistujalistassa')
    consent1 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojen käytön tapahtuman järjestämisessä *', validators=[DataRequired()])
    consent2 = BooleanField('Ymmärrän, että ilmoittautuminen on sitova *', validators=[DataRequired()])

    submit = SubmitField('Ilmoittaudu')


class korttijalautapeliiltaForm(FlaskForm):
    etunimi = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    phone = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
    email = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    
    kilta = SelectField('Kilta *', 
        choices=(['OTiT', 'OTiT'], ['SIK', 'SIK'], ['YMP', 'YMP'], ['KONE', 'KONE'], 
        ['PROSE', 'PROSE'], ['OPTIEM', 'OPTIEM'], ['ARK', 'ARK']))

    consent0 = BooleanField('Sallin nimeni julkaisemisen osallistujalistassa')
    consent1 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojeni käytön tapahtuman järjestämisessä *', validators=[DataRequired()])
    consent2 = BooleanField('Ymmärrän, että ilmoittautuminen on sitova *', validators=[DataRequired()])

    submit = SubmitField('Ilmoittaudu')


class fuksilauluiltaForm(FlaskForm):
    etunimi = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    email = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    
    consent1 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojeni käytön tapahtuman järjestämisessä *', validators=[DataRequired()])

    submit = SubmitField('Ilmoittaudu')


class slumberpartyForm(FlaskForm):
    etunimi = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    phone = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
    email = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    
    kilta = SelectField('Kilta *', 
        choices=(['OTiT', 'OTiT'], ['SIK', 'SIK'], ['YMP', 'YMP'], ['KONE', 'KONE'], 
        ['PROSE', 'PROSE'], ['OPTIEM', 'OPTIEM'], ['ARK', 'ARK']))

    consent0 = BooleanField('Sallin nimeni julkaisemisen osallistujalistassa')
    consent1 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojeni käytön tapahtuman järjestämisessä *', validators=[DataRequired()])
    consent2 = BooleanField('Ymmärrän, että ilmoittautuminen on sitova *', validators=[DataRequired()])

    submit = SubmitField('Ilmoittaudu')



class pakohuoneForm(FlaskForm):

    text0 = 'Pommi (Uusikatu)(vapaa)'
    text1 = 'Kuolleen miehen saari (Uusikatu)(vapaa)'
    text2 = 'Temppelin kirous (Uusikatu)(vapaa)'
    text3 = 'Velhon perintö (Uusikatu)(vapaa)'
    text4 = 'Murhamysteeri (Kajaaninkatu)(vapaa)'
    text5 = 'Vankilapako (Kajaaninkatu)(vapaa)'
    text6 = 'Professorin arvoitus (Kajaaninkatu)(vapaa)'
    text7 = 'The SAW (Kirkkokatu)(vapaa)'
    text8 = 'Alcatraz (Kirkkokatu)(vapaa)'
    text9 = 'Matka maailman ympäri (Kirkkokatu)(vapaa)'
    text10 = 'Pommi (Uusikatu)(vapaa)'
    text11 = 'Kuolleen miehen saari (Uusikatu)(vapaa)'
    text12 = 'Temppelin kirous (Uusikatu)(vapaa)'
    text13 = 'Velhon perintö (Uusikatu)(vapaa)'
    text14 = 'Murhamysteeri (Kajaaninkatu)(vapaa)'
    text15 = 'Vankilapako (Kajaaninkatu)(vapaa)'
    text16 = 'Professorin arvoitus (Kajaaninkatu)(vapaa)'
    text17 = 'The SAW (Kirkkokatu)(vapaa)'
    text18 = 'Alcatraz (Kirkkokatu)(vapaa)'
    text19 = 'Matka maailman ympäri (Kirkkokatu)(vapaa)'


    aika = RadioField('Aika *', 
        choices=(['18:00', '18:00'], ['19:30', '19:30']), 
        validators=[DataRequired()])

    huone1800 = SelectField('Huone (18:00) *', 
        choices=(['Pommi (Uusikatu)', text0], 
        ['Kuolleen miehen saari (Uusikatu)', text1], 
        ['Temppelin kirous (Uusikatu)', text2], 
        ['Velhon perintö (Uusikatu)', text3], 
        ['Murhamysteeri (Kajaaninkatu)', text4], 
        ['Vankilapako (Kajaaninkatu)', text5], 
        ['Professorin arvoitus (Kajaaninkatu)', text6], 
        ['The SAW (Kirkkokatu)', text7], 
        ['Alcatraz (Kirkkokatu)', text8], 
        ['Matka maailman ympäri (Kirkkokatu)', text9],
        ['', '']),
        validators=[RequiredIfValue(other_field_name='aika', value='18:00')], 
        default=(['', '']))

    huone1930 = SelectField('Huone (19:30) *', 
        choices=(['Pommi (Uusikatu)', text10], 
        ['Kuolleen miehen saari (Uusikatu)', text11], 
        ['Temppelin kirous (Uusikatu)', text12], 
        ['Velhon perintö (Uusikatu)', text13], 
        ['Murhamysteeri (Kajaaninkatu)', text14], 
        ['Vankilapako (Kajaaninkatu)', text15], 
        ['Professorin arvoitus (Kajaaninkatu)', text16], 
        ['The SAW (Kirkkokatu)', text17], 
        ['Alcatraz (Kirkkokatu)', text18], 
        ['Matka maailman ympäri (Kirkkokatu)', text19],
        ['', '']),
        validators=[RequiredIfValue(other_field_name='aika', value='19:30')], 
        default=(['', '']))


    etunimi0 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi0 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    phone0 = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
    email0 = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])

    etunimi1 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi1 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])

    etunimi2 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi2 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])

    etunimi3 = StringField('Etunim *', validators=[DataRequired(), length(max=50)])
    sukunimi3 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])

    etunimi4 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi4 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])

    etunimi5 = StringField('Etunimi', validators=[length(max=50)])
    sukunimi5 = StringField('Sukunimi', validators=[length(max=50)])

    consent0 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojeni käytön tapahtuman järjestämisessä *', validators=[DataRequired()])

    submit = SubmitField('Ilmoittaudu')


    def __init__(self, entrys):
        for entry in entrys:
            if(entry.aika == "18:00"):
                if(entry.huone1800 == 'Pommi (Uusikatu)'):
                    self.text0 = 'Pommi (Uusikatu)(varattu)'
                elif(entry.huone1800 == 'Kuolleen miehen saari (Uusikatu)'):
                    self.text1 = 'Kuolleen miehen saari (Uusikatu)(varattu)'
                elif(entry.huone1800 == 'Temppelin kirous (Uusikatu)'):
                    self.text2 = 'Temppelin kirous (Uusikatu)(varattu)'
                elif(entry.huone1800 == 'Velhon perintö (Uusikatu)'):
                    self.text3 = 'Velhon perintö (Uusikatu)(varattu)'
                elif(entry.huone1800 == 'Murhamysteeri (Kajaaninkatu)'):
                    self.text4 = 'Murhamysteeri (Kajaaninkatu)(varattu)'
                elif(entry.huone1800 == 'Vankilapako (Kajaaninkatu)'):
                    self.text5 = 'Vankilapako (Kajaaninkatu)(varattu)'
                elif(entry.huone1800 == 'Professorin arvoitus (Kajaaninkatu)'):
                    self.text6 = 'Professorin arvoitus (Kajaaninkatu)(varattu)'
                elif(entry.huone1800 == 'The SAW (Kirkkokatu)'):
                    self.text7 = 'The SAW (Kirkkokatu)(varattu)'
                elif(entry.huone1800 == 'Alcatraz (Kirkkokatu)'):
                    self.text8 = 'Alcatraz (Kirkkokatu)(varattu)'
                elif(entry.huone1800 == 'Matka maailman ympäri (Kirkkokatu)'):
                    self.text9 = 'Matka maailman ympäri (Kirkkokatu)(varattu)'

            elif(entry.aika == "19:30"):
                if(entry.huone1800 == 'Pommi (Uusikatu)'):
                    self.text10 = 'Pommi (Uusikatu)(varattu)'
                elif(entry.huone1800 == 'Kuolleen miehen saari (Uusikatu)'):
                    self.text11 = 'Kuolleen miehen saari (Uusikatu)(varattu)'
                elif(entry.huone1800 == 'Temppelin kirous (Uusikatu)'):
                    self.text12 = 'Temppelin kirous (Uusikatu)(varattu)'
                elif(entry.huone1800 == 'Velhon perintö (Uusikatu)'):
                    self.text13 = 'Velhon perintö (Uusikatu)(varattu)'
                elif(entry.huone1800 == 'Murhamysteeri (Kajaaninkatu)'):
                    self.text14 = 'Murhamysteeri (Kajaaninkatu)(varattu)'
                elif(entry.huone1800 == 'Vankilapako (Kajaaninkatu)'):
                    self.text15 = 'Vankilapako (Kajaaninkatu)(varattu)'
                elif(entry.huone1800 == 'Professorin arvoitus (Kajaaninkatu)'):
                    self.text16 = 'Professorin arvoitus (Kajaaninkatu)(varattu)'
                elif(entry.huone1800 == 'The SAW (Kirkkokatu)'):
                    self.text17 = 'The SAW (Kirkkokatu)(varattu)'
                elif(entry.huone1800 == 'Alcatraz (Kirkkokatu)'):
                    self.text18 = 'Alcatraz (Kirkkokatu)(varattu)'
                elif(entry.huone1800 == 'Matka maailman ympäri (Kirkkokatu)'):
                    self.text19 = 'Matka maailman ympäri (Kirkkokatu)(varattu)'