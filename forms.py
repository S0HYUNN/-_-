from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, TextAreaField, SelectField

class InForm(FlaskForm):
    user_id = StringField("Username: ")
    type = SelectField("Type of Clothing: ", choices=[('bag','Bag'), ('shirt', 'Shirt'), ('jeans', 'Jeans')])
    tags = TextAreaField(u"Preferred Hashtags: ")
    style = RadioField("Choose Style: ", choices=[('Sungsu', 'Sungsu'), ('Hongdae', 'Hongdae'), ('Gangnam','Gangnam'), ('Sinsa', 'Sinsa')])
    submit = SubmitField()

class Login(FlaskForm):
    username = StringField("Username: ", placeholder="Username")
    submit = SubmitField("SIGN UP")
