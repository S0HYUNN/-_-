
from flask import Flask, render_template, request, send_file, session, redirect
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import InForm
from oauth2client.contrib.flask_util import UserOAuth2
from werkzeug.utils import secure_filename
from sqlalchemy import MetaData, Table, Column, String
from dbconn import get_con

app = Flask(__name__)
###########################
###### DB setup ###########
###########################
app.config['SECRET_KEY'] = 'mysecretkey'

app.config['GOOGLE_OAUTH2_CLIENT_SECRETS_FILE'] = 'secret.json'
#app.config['GOOGLE_OAUTH2_CLIENT_ID'] = os.environ['OAUTH_CLIENT']
#app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = os.environ['OAUTH_SECRET']

oauth2 = UserOAuth2(app)

######## DB Section ##########
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
input_db=SQLAlchemy(app)
Migrate(app, input_db)

# GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", '516475944042-psbar5tjohs8qqdfcjibejuhv9nnscpe.apps.googleusercontent.com')
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", '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')


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

class login(input_db.Model):
    __tablename__ = 'login'
    email = input_db.Column(input_db.Text, primary_key = True)
    name = input_db.Column(input_db.Text)
    
    def __init__(self, email, name):
        self.email = email
        self.name = name
        
    def __repr__(self):
        return f"email : {self.email} name : {self.name}"
    
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

@app.route('/login')
def login():
    test_db = Input.query.all()
    return render_template('login.html', test_db = test_db)

@app.route('/oauth2authorize')
@oauth2.required
def google_oauth():
    print("Google OAuth>> {} ({})".format(oauth2.email, oauth2.user_id))
    print("email : ", oauth2.email)
    print("name : ", oauth2.name)
    return redirect('/')
    # u = User.query.filter('email = : email').params(email=oauth2.email).first()
    # if u is not None:
    #     session['loginUser'] = {'userid' : u.id, 'name' : u.nickname}
    #     return redirect('/')
    
    # else:
    #     flask("해당 사용자가 없습니다!!")
    #     return render_template("login.html", email = oauth2.email)    

@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']
        session.modified = True
        oauth2.storage.delete()
        
    return redirect('/')

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