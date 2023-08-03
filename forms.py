from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, TextAreaField, SelectField

class InForm(FlaskForm):
    user_id = StringField("User ID: ")
    type = SelectField("Type of Clothing: ", choices=[('bag','Bag'), ('shirt', 'Shirt'), ('jeans', 'Jeans')])
    tags = TextAreaField(u"Preferred Hashtags: ")
    price = IntegerField("Price(won)")
    submit = SubmitField()