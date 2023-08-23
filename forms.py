from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, TextAreaField, SelectField

class InForm(FlaskForm):
    type = SelectField("Type of Clothing: ", choices=[('가방','가방'), ('신발', '신발'), ('셔츠', '셔츠'), ('팬츠', '팬츠'), ('코트', '코트'), ('니트', '니트'), ('패딩', '패딩'), ('후드', '후드'), ('바람막이', '바람막이')])
    season = SelectField("What season is your clothing best for?", choices=[("봄코디", "봄"), ("여름코디", "여름"), ("가을코디", "가을"), ("겨울코디", "겨울")])
    style = SelectField("Choose Style: ", choices=[('스트릿', '스트릿'), ('캐주얼', '캐주얼'), ('빈티지','빈티지'), ('트레이닝', '트레이닝'), ('등산', '고프코어')])
    focus = SelectField("Style Focus: ", choices=[("남친룩","남친룩"), ("셋업","셋업"), ("대학생","개강룩"), ("데일리","데일리")])
    submit = SubmitField("Submit")

class Login(FlaskForm):
    username = StringField(render_kw={"placeholder":"Username"})
    submit = SubmitField("SIGN UP")