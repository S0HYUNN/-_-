import os
import pathlib
import pandas as pd
import requests
import google.auth.transport.requests
from oauth2client.contrib.flask_util import UserOAuth2
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from flask import Flask, render_template, request, send_file, session, redirect, abort, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column, String
from forms import InForm, Login
from werkzeug.utils import secure_filename
from sqlalchemy import MetaData, Table, Column, String
from dbconn import get_con
import json
from gensim.models import Word2Vec

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
###########################
###### DB setup ###########
###########################
app.config['SECRET_KEY'] = '1234'

# 세션 설정
# session["state"] = "some_value"

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
    if 'email' in session:
        sql= f"select username from login where email='{session['email']}'"
        conn = get_con()
        sql_result = pd.read_sql(sql, conn)
        result = sql_result.to_dict('records')
        
        if result:  # result 리스트에 요소가 있는 경우
            session['username'] = result[-1]['username']
            print(session['username'])
        return render_template('index.html', username=session.get('username'))
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
    callback_flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri="http://localhost:5000/callback"
    )

    callback_flow.fetch_token(authorization_response=request.url)
    credentials = callback_flow.credentials
    token_request = google.auth.transport.requests.Request()

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
        return redirect(url_for('index'))  # main page로 redirect

    return redirect(url_for('signup'))  # signup page로 redirect

@app.route('/signup', methods=['GET','POST'])
def signup():
    #     # 임시
    session["email"]="jiwoongmun@gmail.com"
    session["name"] = "Jiwoong"
    ## 회원 가입 절차 시작 ##
    form = Login()
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
            return redirect(url_for("index")) ## input main page로
    return render_template('signup_copy.html', form=form, email=session['email'], name=session['name'])
   

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route('/input', methods=['GET','POST'])
def input():
    if not ('name' in session):
        flash("로그인을 해주세요")
        return redirect(url_for("index"))

    form = InForm()
    if form.validate_on_submit():
        username = session['username']
        type = form.type.data
        season = form.season.data
        style = form.style.data
        focus = form.focus.data
        session['type'] = type
        session['season'] = season
        session['style'] = style
        session['focus'] = focus


        meta = MetaData()
        new_user = Table(
            "input_db", meta, 
            Column("username", String),
            Column("type", String),
            Column("season", String),
            Column("style", String),
            Column("focus", String)
            )
        ins = new_user.insert().values(username=username, type=type, season=season, style = style, focus = focus)
        conn = get_con()
        conn.execute(ins)
        return redirect(url_for("output"))
    return render_template("input.html", form=form, username=session.get('username'))

@app.route('/get_rel_word', methods=['GET', 'POST'])
def get_rel_word():
    # 파라미터
    # keyword = [session['type'], session['season'], session['style'], session['focus'] ]
    keyword_param = json.loads(request.data)
    print(keyword_param)
    # 모델
    model = Word2Vec.load("data_working/model/Word2Vec.model")
    result = model.wv.most_similar(positive=keyword_param.get("keyword"), topn=10)
    print("___________________")
    print(result)
    return json.dumps(result,ensure_ascii=False)

@app.route("/influencer", methods=['GET', 'POST'])
def influencer():
    param = json.loads(request.data)
    print(param)
    # key1 = data.get("key1")
    sql = "select username,\
                    ((key1_rn+key2_rn+key3_rn)/3*2)+((cnt1_rn+cnt2_rn+cnt3_rn+cnt4_rn+cnt5_rn+cnt6_rn+cnt7_rn+cnt8_rn+cnt9_rn+cnt10_rn)/10) as score\
                from (\
                select username,\
                        rank() over(order by key1) as key1_rn,\
                        rank() over(order by key2) as key2_rn,\
                        rank() over(order by key3) as key3_rn,\
                        rank() over(order by cnt1) as cnt1_rn,\
                        rank() over(order by cnt2) as cnt2_rn,\
                        rank() over(order by cnt3) as cnt3_rn,\
                        rank() over(order by cnt4) as cnt4_rn,\
                        rank() over(order by cnt5) as cnt5_rn,\
                        rank() over(order by cnt6) as cnt6_rn,\
                        rank() over(order by cnt7) as cnt7_rn,\
                        rank() over(order by cnt8) as cnt8_rn,\
                        rank() over(order by cnt9) as cnt9_rn,\
                        rank() over(order by cnt10) as cnt10_rn\
                from\
                (\
                    select username,\
                            (length(cap) - length(replace(cap, '"+param.get('keyword')[0]+"' , ''))) as key1,\
                            (length(cap) - length(replace(cap, '"+param.get('keyword')[1]+"' , ''))) as key2,\
                            (length(cap) - length(replace(cap, '"+param.get('keyword')[2]+"' , ''))) as key3,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[0]+"' , ''))) as cnt1,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[1]+"' , ''))) as cnt2,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[2]+"' , ''))) as cnt3,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[3]+"' , ''))) as cnt4,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[4]+"' , ''))) as cnt5,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[5]+"' , ''))) as cnt6,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[6]+"' , ''))) as cnt7,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[7]+"' , ''))) as cnt8,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[8]+"' , ''))) as cnt9,\
                            (length(cap) - length(replace(cap, '"+param.get('rel_keyword')[9]+"' , ''))) as cnt10\
                    from\
                    (\
                        select username,array_to_string(array_agg(caption),',') as cap\
                        from major_media\
                        group by username\
                        union all\
                        select username,array_to_string(array_agg(caption),',') as cap\
                        from minor_media\
                        group by username\
                    ) tab\
                ) tab\
            ) tab"
    
    conn = get_con()
    sql_result = pd.read_sql(sql, conn)
    hashtags = sql_result.to_dict('records')

    return json.dumps(hashtags, ensure_ascii=False)


@app.route('/projects')
def projects():
    if not ('name' in session):
        flash("로그인을 해주세요")
        return redirect(url_for("index"))
    sql=f"select type, focus, style, season from input_db where username='{session['username']}'"
    conn = get_con()
    sql_result = pd.read_sql(sql, conn)
    result = sql_result.to_dict('records')
    return render_template('projects_copy.html', projects=result, username=session.get('username'))

@app.route('/projects-output')
def projects_output():
    Ptype= request.args.get("Ptype")
    Pseason= request.args.get("Pseason")
    Pstyle = request.args.get("Pstyle")
    Pfocus = request.args.get("Pfocus")
        # inf_name = json.loads(request.data)
    sql1= f"select year_month, comments_count_mean, like_count_mean from full_date where username='jiseong'"
    sql2 = f"select media_product_type, media_type, comments_count_mean, like_count_mean from full_type where username='jiseong'"
    conn = get_con()
    sql_result1 = pd.read_sql(sql1, conn)
    sql_result2 = pd.read_sql(sql2, conn)
    result1 = sql_result1.to_dict('records')
    result2 = sql_result2.to_dict('records')

    graph_data = json.dumps({'result1':result1,'result2':result2}, ensure_ascii=False)
    print(graph_data)
    sql="select username, followers_count, media_count from total_person "
    sql_result = pd.read_sql(sql, conn)
    people = sql_result.to_dict('records')
    print(people)
    return render_template('output_copy.html', name=session['name'], username=session.get('username'), type=Ptype ,season=Pseason, style=Pstyle, focus=Pfocus, people=people, data= graph_data)

@app.route('/output', methods=['GET', 'POST'])
def output():
    # inf_name = json.loads(request.data)
    sql1= f"select year_month, comments_count_mean, like_count_mean from full_date where username='jiseong'"
    sql2 = f"select media_product_type, media_type, comments_count_mean, like_count_mean from full_type where username='jiseong'"
    conn = get_con()
    sql_result1 = pd.read_sql(sql1, conn)
    sql_result2 = pd.read_sql(sql2, conn)
    result1 = sql_result1.to_dict('records')
    result2 = sql_result2.to_dict('records')

    graph_data = {
        'result1': result1,
        'result2': result2
    }
   
    sql="select username, followers_count, media_count from total_person "
    sql_result = pd.read_sql(sql, conn)
    people = sql_result.to_dict('records')
    # print(people)
    return render_template('output_copy.html', name=session['name'], username=session.get('username'), type=session['type'] ,season=session['season'], style=session['style'], focus=session['focus'], people=people, data=json.dumps(graph_data))


@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/resume')
def resume():
    return render_template('resume.html', name=session['name'], username=session.get('username'))

@app.route('/major')
def major():
    influencer= request.args.get("influencer")
    sql1 = f"select * from inf_info where username='{influencer}'"
    sql2 = f"select * from chk_power_total where username='{influencer}'"
    sql3 = f"select followers_count, media_count from total_person where username='{influencer}'"

    conn=get_con()
    sql_result1 = pd.read_sql(sql1, conn)
    result1 = sql_result1.to_dict('records')
    sql_result2 = pd.read_sql(sql2, conn)
    result2 = sql_result2.to_dict('records')
    sql_result3 = pd.read_sql(sql3, conn)
    result3 = sql_result3.to_dict('records')

    influencer_stuff = json.dumps({'result1':result1,'result2':result2, 'result3':result3}, ensure_ascii=False)
    influencer_stuff = json.loads(influencer_stuff)

    return render_template('major.html', inf_info=influencer_stuff)

@app.route('/minor')
def minor():
    influencer= request.args.get("influencer")
    sql1 = f"select * from inf_info where username='{influencer}'"
    sql2 = f"select * from chk_power_total where username='{influencer}'"
    sql3 = f"select followers_count, media_count from total_person where username='{influencer}'"

    conn=get_con()
    sql_result1 = pd.read_sql(sql1, conn)
    result1 = sql_result1.to_dict('records')
    sql_result2 = pd.read_sql(sql2, conn)
    result2 = sql_result2.to_dict('records')
    sql_result3 = pd.read_sql(sql3, conn)
    result3 = sql_result3.to_dict('records')

    influencer_stuff = json.dumps({'result1':result1,'result2':result2, 'result3':result3}, ensure_ascii=False)
    influencer_stuff = json.loads(influencer_stuff)

    return render_template('minor.html', inf_info=influencer_stuff)

@app.route('/minor2')
def minor2():
    influencer= request.args.get("influencer")
    sql1 = f"select * from inf_info where username='{influencer}'"
    sql2 = f"select * from chk_power_total where username='{influencer}'"
    sql3 = f"select followers_count, media_count from total_person where username='{influencer}'"

    conn=get_con()
    sql_result1 = pd.read_sql(sql1, conn)
    result1 = sql_result1.to_dict('records')
    sql_result2 = pd.read_sql(sql2, conn)
    result2 = sql_result2.to_dict('records')
    sql_result3 = pd.read_sql(sql3, conn)
    result3 = sql_result3.to_dict('records')

    influencer_stuff = json.dumps({'result1':result1,'result2':result2, 'result3':result3}, ensure_ascii=False)
    influencer_stuff = json.loads(influencer_stuff)

    return render_template('minor2.html', inf_info=influencer_stuff)

if __name__ == '__main__':
    app.run(port="5000", debug = True)