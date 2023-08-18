import os
import pathlib
import pandas as pd
import requests
import google.auth.transport.requests
from oauth2client.contrib.flask_util import UserOAuth2
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from flask import Flask, render_template, request, send_file, session, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column, String
from forms import InForm, Login
from werkzeug.utils import secure_filename
from sqlalchemy import MetaData, Table, Column, String
from dbconn import get_con
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
###########################
###### DB setup ###########
###########################
app.config['SECRET_KEY'] = '1234'

app.config['JSON_AS_ASCII'] = False
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "516475944042-psbar5tjohs8qqdfcjibejuhv9nnscpe.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri = "http://localhost:5000/callback"
    )

##############################################################################
##                                  사이트 구현                                ##
##############################################################################


##              메인 페이지              ##
@app.route('/', methods=['GET', 'POST'])
def index():    
    if 'name' in session:
        return render_template('index.html', name=session['name'])
    else:
        return render_template('index.html')

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function() 
             
    return wrapper

##               로그인 페이지              ##

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)
    # session["google_id"] = "Test"
    # return redirect("/protected_area")

##               회원정보 확인 or 회원가입              ##

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)



    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    if not (session["state"] == request.args["state"]):
        abort(500)  # State does not match!
        
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    email = id_info.get("email")
    name = id_info.get("name")
    session["email"] = email
    session["name"] = name
    ## 이미 회원인지 확인
    sql = "select email from login"
    conn = get_con()
    sql_result = pd.read_sql(sql, conn)
    result = sql_result.to_dict('records')
    email_list = [record["email"] for record in result]
    if email in email_list:
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        return redirect("/") ## input main page로 redirect

    return redirect("signup.html") 

@app.route('/signup', methods=['GET','POST'])
def signup():
    ## 회원 가입 절차 시작 ##
    form = Login()
        ## 임시
    session['email'] = 'jiwoongmun@gmail.com'
    session['name'] = 'jiwoong'
    if form.validate_on_submit():
        username= form.username.data
        ## username unique 한지 확인
        sql = "select username from login"
        conn = get_con()
        sql_result = pd.read_sql(sql, conn)
        result = sql_result.to_dict('records')
        username_list = [record['username'] for record in result]
        if (username in username_list):
            ## 이 방법 말고 페이지에서 바로 보여주는 방법을 찾자!
            return '<h1>Username already taken! </h1>'
        else:
        ## DB insert
            meta = MetaData()
            new_user = Table(
                "login", meta, 
                Column("email", String),
                Column("name", String),
                Column("username", String)
                )
            ins = new_user.insert().values(email=session['email'], name=session['name'], username=username)
            conn = get_con()
            conn.execute(ins)
            return redirect("/") ## input main page로
    return render_template('signup.html', form=form, email=session['email'], name=session['name'] )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/protected_area")
@login_is_required
def protected_area():
    return "Protected! <a href='/logout'><button>Logout</button></a>"


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/major')
def major():
    return render_template('major.html')

@app.route('/minor')
def minor():
    return render_template('minor.html')

@app.route('/minor2')
def minor2():
    return render_template('minor2.html')

@app.route('/output')
def output():
    return render_template('output.html')
@app.route('/base')
def base():
    return render_template('base.html')
if __name__ == '__main__':
    app.run(port="5000", debug = True)