from unittest import result
from urllib import request
from flask import Flask
from flask import render_template,request
import ibm_db
app = Flask(__name__)


@app.route("/")
@app.route("/",methods=["POST"])
def register():
    if request.method=="POST":  
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fbc81880;PWD=v4TioNbfWbm9MZP7;","","")
        result=request.form
        email=result.get('Email')
        username=result.get('UserName')
        password=result.get('Password')
        phoneNumber=result.get('PhoneNumber')
        sql = "insert into users values('"+phoneNumber+"','"+username+"','"+email+"','"+password+"')"
        ibm_db.exec_immediate(conn,sql)
        return render_template("Login.html")
    return render_template("signup1.html")

@app.route("/login")
@app.route("/login",methods=['POST'])
def login():
    if request.method=="POST":  
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fbc81880;PWD=v4TioNbfWbm9MZP7;","","")
        result=request.form
        email=result.get('Email')
        password=result.get('Password')
        sql="select username from users where email='"+email+"'and password = '"+password+"'"
        stmt=ibm_db.exec_immediate(conn,sql)
        out=ibm_db.fetch_tuple(stmt)
        if out!=None:
            return render_template("welcome.html",result=out)     
    return render_template("Login.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8000,debug=True)
