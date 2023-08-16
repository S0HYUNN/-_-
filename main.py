import os
import pathlib

import google.auth.transport.requests
import requests
from flask import Flask, render_template, request, send_file, session, redirect, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import InForm
from oauth2client.contrib.flask_util import UserOAuth2
from werkzeug.utils import secure_filename
from sqlalchemy import MetaData, Table, Column, String
from dbconn import get_con
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
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


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "516475944042-psbar5tjohs8qqdfcjibejuhv9nnscpe.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri = "http://localhost:5000/callback"
    )

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
    
    if 'name' in session:
        return render_template('index.html', name=session['name'], form=form)
    else:
        return render_template('index.html', form=form)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function() 
             
    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)
    # session["google_id"] = "Test"
    # return redirect("/protected_area")

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    email = id_info.get("email")
    name = id_info.get("name")

    # return f"Email: {email}, Name: {name} <a href='/'><button>main</button></a>"

    # return id_info
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/protected_area")
@login_is_required
def protected_area():
    return "Protected! <a href='/logout'><button>Logout</button></a>"


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

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(port="5000", debug = True)