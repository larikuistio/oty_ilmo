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

    #aika = None
    #huone1800 = None
    #huone1930 = None
    #etunimi0 = None
    #sukunimi0 = None
    #phone0 = None
    #email0 = None
    #etunimi1 = None
    #sukunimi1 = None
    #etunimi2 = None
    #sukunimi2 = None
    #etunimi3 = None
    #sukunimi3 = None
    #etunimi4 = None
    #sukunimi4 = None
    #etunimi5 = None
    #sukunimi5 = None
    #consent0 = None
    #submit = None
    
    def __init__(self, texts, *args, **kwargs):

        super(pakohuoneForm, self).__init__(*args, **kwargs)

        self.aika = RadioField('Aika *', 
            choices=(['18:00', '18:00'], ['19:30', '19:30']), 
            validators=[DataRequired()])

        self.huone1800 = SelectField('Huone (18:00) *', 
            choices=(['Pommi (Uusikatu)', texts[0]], 
            ['Kuolleen miehen saari (Uusikatu)', texts[1]], 
            ['Temppelin kirous (Uusikatu)', texts[2]], 
            ['Velhon perintö (Uusikatu)', texts[3]], 
            ['Murhamysteeri (Kajaaninkatu)', texts[4]], 
            ['Vankilapako (Kajaaninkatu)', texts[5]], 
            ['Professorin arvoitus (Kajaaninkatu)', texts[6]], 
            ['The SAW (Kirkkokatu)', texts[7]], 
            ['Alcatraz (Kirkkokatu)', texts[8]], 
            ['Matka maailman ympäri (Kirkkokatu)', texts[9]],
            ['', '']),
            validators=[RequiredIfValue(other_field_name='aika', value='18:00')], 
            default=(['', '']))

        self.huone1930 = SelectField('Huone (19:30) *', 
            choices=(['Pommi (Uusikatu)', texts[10]], 
            ['Kuolleen miehen saari (Uusikatu)', texts[11]], 
            ['Temppelin kirous (Uusikatu)', texts[12]], 
            ['Velhon perintö (Uusikatu)', texts[13]], 
            ['Murhamysteeri (Kajaaninkatu)', texts[14]], 
            ['Vankilapako (Kajaaninkatu)', texts[15]], 
            ['Professorin arvoitus (Kajaaninkatu)', texts[16]], 
            ['The SAW (Kirkkokatu)', texts[17]], 
            ['Alcatraz (Kirkkokatu)', texts[18]], 
            ['Matka maailman ympäri (Kirkkokatu)', texts[19]],
            ['', '']),
            validators=[RequiredIfValue(other_field_name='aika', value='19:30')], 
            default=(['', '']))


        self.etunimi0 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
        self.sukunimi0 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
        self.phone0 = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
        self.email0 = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])

        self.etunimi1 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
        self.sukunimi1 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])

        self.etunimi2 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
        self.sukunimi2 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])

        self.etunimi3 = StringField('Etunim *', validators=[DataRequired(), length(max=50)])
        self.sukunimi3 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])

        self.etunimi4 = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
        self.sukunimi4 = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])

        self.etunimi5 = StringField('Etunimi', validators=[length(max=50)])
        self.sukunimi5 = StringField('Sukunimi', validators=[length(max=50)])

        self.consent0 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojeni käytön tapahtuman järjestämisessä *', validators=[DataRequired()])

        self.submit = SubmitField('Ilmoittaudu')


    