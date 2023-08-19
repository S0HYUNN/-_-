from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, TextAreaField, SelectField

class InForm(FlaskForm):
    type = SelectField("Type of Clothing: ", choices=[('bag','Bag'), ('shirt', 'Shirt'), ('jeans', 'Jeans')])
    season = SelectField("What season is your clothing best for?", choices=[("봄코디", "봄"), ("여름코디", "여름"), ("가을코디", "가을"), ("겨울코디", "겨울")])
    style = SelectField("Choose Style: ", choices=[('스트릭', '스트릿'), ('캐주얼', '캐주얼'), ('빈티지','빈티지'), ('럭셔리', '럭셔리'), ("스포츠웨어","스포츠웨어"), ("Y2K","Y2K"),("올드머니","올드머니")])
    focus = SelectField("Style Focus: ", choices=[("남친룩","남친룩"), ("꾸안꾸","꾸안꾸"), ("셋업","셋업"), ("해변룩","해변룩")])
    submit = SubmitField("Submit")

class Login(FlaskForm):
    username = StringField(render_kw={"placeholder":"Username"})
    submit = SubmitField("SIGN UP")