from app import db, login_manager
from datetime import date
from flask_login import UserMixin
import ibm_db
@login_manager.user_loader
def load_user(user_id):
    sql="select * from user where id=? limit 1;"
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=fbc81880;PWD=v4TioNbfWbm9MZP7;","","")
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,user_id)
    ibm_db.execute(stmt)
    users=ibm_db.fetch_both(stmt)
    return User(users[0],users[1],users[2],users[3],users[4])


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    usertype = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    jobs = db.relationship('Jobs', backref='job_applier', lazy=True)
    applications = db.relationship('Application', backref='application_submiter', lazy=True)

    def __init__(self,id,username,usertype,email,password):
        self.id=id
        self.username=username
        self.usertype=usertype
        self.email=email
        self.password=password
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.usertype}', '{self.email}')"

