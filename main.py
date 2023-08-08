from flask import Flask, render_template, url_for, redirect, session, request, send_file
import pandas as pd
from dbconn import get_con
import requests
from sqlalchemy import MetaData, Table, Column, String
from forms import InForm
import uuid
import json


app = Flask(__name__)
###########################
###### DB setup ###########
###########################
app.secret_key = "levware!1234"



@app.route('/', methods=['GET', 'POST'])
def index():
    form = InForm()
    # 받아온 input으로 class instance 만들고 db에 저장
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
        # new_input = Input(user_id, type, tags , style)
        # input_db.session.add(new_input)
        # input_db.session.commit()
        return redirect(url_for('list'))
    return render_template('index.html', form=form)

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




######## DB Section ##########
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# input_db=SQLAlchemy(app)
# Migrate(app, input_db)

######## MODELS ##############
# class Input(input_db.Model):
#     __tablename__ = 'input'
#     id = input_db.Column(input_db.Integer, primary_key = True)
#     user_id = input_db.Column(input_db.Text)
#     type = input_db.Column(input_db.Text)
#     tags = input_db.Column(input_db.Text)
#     style = input_db.Column(input_db.Integer)

#     def __init__(self, user_id, type, tags, style):
#         self.user_id = user_id
#         self.type = type
#         self.tags = tags
#         self.style = style
    
#     def __repr__(self):
#         return f"{self.type}: {self.tags}"