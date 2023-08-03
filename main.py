from flask import Flask, render_template, url_for, redirect, session
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import InForm
app = Flask(__name__)
###########################
###### DB setup ###########
###########################
app.config['SECRET_KEY'] = 'mysecretkey'

######## DB Section ##########
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
input_db=SQLAlchemy(app)
Migrate(app, input_db)

######## MODELS ##############
class Input(input_db.Model):
    __tablename__ = 'input'
    id = input_db.Column(input_db.Integer, primary_key = True)
    user_id = input_db.Column(input_db.Text)
    type = input_db.Column(input_db.Text)
    tags = input_db.Column(input_db.Text)
    price = input_db.Column(input_db.Integer)

    def __init__(self, user_id, type, tags, price):
        self.user_id = user_id
        self.type = type
        self.tags = tags
        self.price = price
    
    def __repr__(self):
        return f"{self.type}: {self.price}won"


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InForm()
    # 받아온 input으로 class instance 만들고 db에 저장
    if form.validate_on_submit():
        user_id = form.user_id.data
        type = form.type.data
        tags = form.tags.data
        price = form.price.data
        new_input = Input(user_id, type, tags , price)
        input_db.session.add(new_input)
        input_db.session.commit()
        return redirect(url_for('list'))
    return render_template('index.html', form=form)

@app.route('/list')
def list():
    test_db = Input.query.all()
    return render_template('list.html', test_db = test_db)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

if __name__ == '__main__':
    app.run(port="5000", debug = True)