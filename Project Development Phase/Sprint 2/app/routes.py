from flask import render_template, url_for, flash, redirect, request, send_file
from app import  app, bcrypt
from PIL import Image
import os
import secrets
from app.form import RegistrationForm, LoginForm, ReviewForm, JobForm, ApplicationForm,ProfileUpdateForm
from app.models import User, Jobs, Review, Application
from flask_login import login_user, current_user, logout_user, login_required
import random
import ibm_db
import datetime



@app.route("/register", methods=['GET', 'POST'])
def register():
    #sprint1

@app.route("/login", methods=['GET', 'POST'])
def login():
    #sprint2

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_jobs'))

def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/post_cvs/<jobid>", methods=['GET', 'POST'])
@login_required
def post_cvs(jobid):
    form = ApplicationForm()
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=fIBM_UID;PWD=IBM_PID;"","","")
    if form.validate_on_submit():
        sql1="insert into application(user_id,job_id,cover_letter,cv) values(?,?,?,?)"
        stmt=ibm_db.prepare(conn,sql1)
        ibm_db.bind_param(stmt,1,current_user.id)
        ibm_db.bind_param(stmt,2,jobid)
        ibm_db.bind_param(stmt,4,form.cv.data.filename)
        ibm_db.bind_param(stmt,3,form.cover_letter.data)
        
        ibm_db.execute(stmt)
        save_picture(form.cv.data)
        flash('Resume uploaded successfully.', 'danger')
        return redirect(url_for('show_jobs'))
    return render_template('post_cvs.html', form=form)

@app.route("/post_jobs", methods=['GET', 'POST'])
@login_required
def post_jobs():
    form = JobForm()
    print("before entered")
    if form.validate_on_submit():
        print("after entered")
        sql="insert into job(title,industry,description,user_id,required_skill) values(?,?,?,?,?)"
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;"","","")
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,form.title.data)
        ibm_db.bind_param(stmt,2,form.industry.data)
        ibm_db.bind_param(stmt,3,form.description.data)
        ibm_db.bind_param(stmt,4,current_user.id)
        ibm_db.bind_param(stmt,5,form.required_skill.data)
        ibm_db.execute(stmt)
        integrateMail(form.title.data,form.description.data,form.required_skill.data)
        return redirect(url_for('posted_jobs'))
    return render_template('post_jobs.html', form=form)

@app.route("/updateprofile" , methods=['GET',"POST"])
@login_required
def updateprofile():
    if current_user.usertype=="Job Seeker":
        form=ProfileUpdateForm()
        if form.validate_on_submit():
            sql="insert into jobseeker values(?,?,?,?,?,?,?)"
            conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;"","","")
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,current_user.id)
            ibm_db.bind_param(stmt,2,form.gender.data)
            ibm_db.bind_param(stmt,3,form.degree.data)
            ibm_db.bind_param(stmt,4,form.experience.data)
            ibm_db.bind_param(stmt,5,form.skill1.data)
            ibm_db.bind_param(stmt,6,form.skill2.data)
            ibm_db.bind_param(stmt,7,form.skill3.data)
            ibm_db.execute(stmt)
            return redirect(url_for('login'))
        return render_template("profile_update.html",form=form)

