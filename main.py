import os
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from flask import Flask, render_template, url_for, redirect, session, request, send_file, abort
import pandas as pd
from dbconn import get_con
import requests
from sqlalchemy import MetaData, Table, Column, String
from forms import InForm, Login
import uuid
import json


app = Flask(__name__)
app.secret_key = "levware!1234"
## for login ##
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


##              로그인 전 페이지              ##

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InForm()
    if form.validate_on_submit():
        uid = uuid.uuid4()
        user_id = form.user_id.data
        type = form.type.data
        tags = form.tags.data
        style = form.style.data

        meta = MetaData()

        new_input = Table(
            "input_db", meta,
            Column("uid", String),
            Column("user_id", String),
            Column("type", String),
            Column("tags", String),
            Column("style", String)
        )

        ins = new_input.insert().values(uid=uid, user_id=user_id, type=type, tags=tags, style=style)
        conn = get_con()
        conn.execute(ins)
        return redirect(url_for('list'))
    return render_template('index.html', form=form)


##               로그인 페이지              ##

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


##               회원정보 확인 or 회원가입              ##

@app.route("/callback", methods=['GET', 'POST'])
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
    ## 이미 회원인지 확인
    sql = "select email from login"
    conn = get_con()
    sql_result = pd.read_sql(sql, conn)
    result = sql_result.to_dict('records')
    email_list = [record["email"] for record in result]
    if email in email_list:
        return redirect() ## main page로 redirect

    form = Login()
    if form.validate_on_submit():
        username= form.username.data

        meta = MetaData()
        new_user = Table(
            "login", meta, 
            Column("email", String),
            Column("name", String)
        )
        ins = new_user.insert().values(email=email, name=name, username=username)
        conn = get_con()
        conn.execute(ins)
        return redirect() ## main page로
    return render_template()    ##form 보여주는 회원가입 페이지


## login 후 mainpage


## log-out
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


##               회원정보 확인 or 회원가입              ##

@app.route('/list')
def list():
    sql = "select uid,user_id,type,tags, style from input_db limit 5"
    conn = get_con()
    sql_result = pd.read_sql(sql, conn)
    result = sql_result.to_dict('records')
    test_db = json.dumps(result, ensure_ascii=False)
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