from flask import Flask, render_template, session
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import InForm

## setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

## DB setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
input_db = SQLAlchemy(app)
Migrate(app, input_db)


class Input(input_db.Model):
    __tablename__ = 'input'
    id = input_db.Column(input_db.Integer, primary_key = True)
    user_id = input_db.Column(input_db.Text)
    type = input_db.Column(input_db.Text)
    tags = input_db.Column(input_db.Text)

    def __init__(self, user_id, type, tags, price):
        self.user_id = user_id
        self.type = type
        self.tags = tags
    
    def __repr__(self):
        return f"{self.type}: {self.price}won"

@app.route('/', methods=['GET','POST']) 
def index():
    form=InForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        type = form.type.data
        tags = form.tags.data
        new_input = Input(user_id, type, tags)
        input_db.session.add(new_input)
        input_db.session.commit()
    return render_template( 'input.html', form=form )

if __name__ == '__main__':
    app.run(port="5000", debug = True)