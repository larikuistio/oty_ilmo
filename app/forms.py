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




class sitsiForm(FlaskForm):
    etunimi = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    email = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    alkoholi = RadioField('Alkoholillinen/Alkoholiton *', 
        choices=(['Alkoholillinen', 'Alkoholillinen'], ['Alkoholiton', 'Alkoholiton']),
       validators=[DataRequired()])
    mieto = SelectField('Mieto juoma *', 
        choices=(['Olut', 'Olut'], ['Siideri', 'Siideri']), 
        validators=[RequiredIf(other_field_name='alkoholi', value="Alkoholillinen")])
    pitsa = SelectField('Pitsa *', 
        choices=(['Liha', 'Liha'], ['Kana', 'Kana'], ['Vege', 'Vege']),
        validators=[DataRequired()])
    allergiat = StringField('Erityisruokavaliot/allergiat', validators=[length(max=200)])
    consent0 = BooleanField('Hyväksyn nimeni julkaisemisen tällä sivulla')
    consent1 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojeni käytön tapahtuman järjestämisessä *', validators=[DataRequired()])

    submit = SubmitField('Ilmoittaudu')


class fucuForm(FlaskForm):
    etunimi = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    email = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    puh = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
    lahtopaikka = SelectField('Lähtöpaikka *', 
        choices=(['Yliopisto', 'Yliopisto'], ['Merikoskenkatu (tuiran bussipysäkki)', 'Merikoskenkatu (tuiran bussipysäkki)'], 
        ['Linja-autoasema', 'Linja-autoasema']), 
        validators=[DataRequired()])
    kiintio = SelectField('Kiintiö *', 
        choices=(['Fuksi', 'Fuksi'], ['Pro', 'Pro'], ['Hallitus', 'Hallitus'], ['Muu', 'Muu']), 
        validators=[DataRequired()])
    consent0 = BooleanField('Hyväksyn nimeni julkaisemisen tällä sivulla')
    consent1 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojeni käytön tapahtuman järjestämisessä *', validators=[DataRequired()])

    submit = SubmitField('Ilmoittaudu')


class kmpForm(FlaskForm):
    etunimi = StringField('Etunimi *', validators=[DataRequired(), length(max=50)])
    sukunimi = StringField('Sukunimi *', validators=[DataRequired(), length(max=50)])
    email = StringField('Sähköposti *', validators=[DataRequired(), Email(), length(max=100)])
    puh = StringField('Puhelinnumero *', validators=[DataRequired(), length(max=20)])
    lahtopaikka = SelectField('Lähtöpaikka *', 
        choices=(['Yliopisto', 'Yliopisto'], ['Merikoskenkatu (tuiran bussipysäkki)', 'Merikoskenkatu (tuiran bussipysäkki)'], 
        ['Linja-autoasema', 'Linja-autoasema']), 
        validators=[DataRequired()])
    consent0 = BooleanField('Hyväksyn nimeni julkaisemisen tällä sivulla')
    consent1 = BooleanField('Olen lukenut tietosuojaselosteen ja hyväksyn tietojeni käytön tapahtuman järjestämisessä *', validators=[DataRequired()])
    consent2 = BooleanField('Ymmärrän, että ilmoittautuminen on sitova ja sitoudun maksamaan 40 euron (ei sisällä sitsien hintaa) maksun killalle *', validators=[DataRequired()])

    submit = SubmitField('Ilmoittaudu')