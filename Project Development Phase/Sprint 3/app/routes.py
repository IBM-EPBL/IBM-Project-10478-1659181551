from flask import render_template, url_for, flash, redirect, request
from app import  app, bcrypt
import os
from app.form import RegistrationForm, LoginForm, ReviewForm, JobForm, ApplicationForm,ProfileUpdateForm
from app.models import User, Jobs, Application
from flask_login import login_user, current_user, logout_user, login_required
import ibm_db
from app.sendmail import sendMail



"""       sprint 1 and 2       """

@app.route("/review", methods=['GET', 'POST'])
@login_required
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        sql="insert into review(username,review) values(?,?)"
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,form.username.data)
        ibm_db.bind_param(stmt,2,form.review.data)
        ibm_db.execute(stmt)
        flash('Thank you for providing the review!', 'success')
        return redirect(url_for('show_jobs'))
    return  render_template('review.html', form=form)

@app.route("/posted_jobs")
@login_required
def posted_jobs():
    sql="select * from job where user_id=?"
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,current_user.id)
    ibm_db.execute(stmt)
    job=ibm_db.fetch_both(stmt)
    jobs=[]
    while job!=False:
        jobs.append(Jobs(job["ID"],job["TITLE"],job["INDUSTRY"],job["DATE_POSTED"],job["DESCRIPTION"]))
        job = ibm_db.fetch_both(stmt)
    return render_template('show_jobs.html', jobs=jobs)


@app.route("/show_applications/<jobid>", methods=['GET'])
@login_required
def show_applications(jobid):
    sql="select * from application where job_id=? order by degree,experience desc"
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,jobid)
    ibm_db.execute(stmt)
    application=ibm_db.fetch_both(stmt)
    applications=[]
    while application!=False:
        applications.append(Application(application["ID"],application["GENDER"],application["DATE_POSTED"],application["DEGREE"],application["INDUSTRY"],application["EXPERIENCE"],application["USER_ID"],application["JOB_ID"]))
        application = ibm_db.fetch_both(stmt)
    return render_template('show_applications.html', applications=applications)

@app.route("/meeting/<application_id>")
@login_required
def meeting(application_id):
    return render_template('meeting.html')

@app.route("/")
@app.route("/show_jobs")
def show_jobs():
    sql="select * from job"
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.execute(stmt)
    job=ibm_db.fetch_both(stmt)
    jobs=list()
    while job!=False:
        jobs.append(Jobs(job["ID"],job["TITLE"],job["INDUSTRY"],job["DATE_POSTED"],job["DESCRIPTION"]))
        job = ibm_db.fetch_both(stmt)
    return render_template('show_jobs.html', jobs=jobs)

@app.route("/resume/<id>", methods=['GET'])
def resume(id):
    sql="select cv from application where id=?"
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,id)
    ibm_db.execute(stmt)
    c=ibm_db.fetch_both(stmt)
    cv=""
    while c!=False:
        cv=c[0]
        c = ibm_db.fetch_both(stmt)
    return render_template('resume.html', cv=cv, id=id)

@app.route("/updateprofile" , methods=['GET',"POST"])
@login_required
def updateprofile():
    if current_user.usertype=="Job Seeker":
        form=ProfileUpdateForm()
        if form.validate_on_submit():
            sql="insert into jobseeker values(?,?,?,?,?,?,?)"
            conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
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


@app.route("/show_application", methods=['GET'])
@login_required
def show_application():
    sql="select * from application inner join job on job.id=application.job_id where application.user_id=? order by date_applied desc"
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,current_user.id)
    ibm_db.execute(stmt)
    application=ibm_db.fetch_both(stmt)
    applications=[]
    while application!=False:
        applications.append(Application(application["ID"],application["DATE_POSTED"],application["USER_ID"],application["JOB_ID"]))
        application = ibm_db.fetch_both(stmt)
    return render_template('show_applications.html', applications=applications)


def integrateMail(title,description,skill):
    sql="select distinct(u.email) from jobseeker as j inner join user as u on j.id=u.id  where j.skill1=? or j.skill2=? or j.skill3=?;"
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
    stmt=ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,skill)
    ibm_db.bind_param(stmt,2,skill)
    ibm_db.bind_param(stmt,3,skill)
    ibm_db.execute(stmt)
    emails=[]
    email=ibm_db.fetch_both(stmt)
    while email:
        emails.append(email[0])
        email=ibm_db.fetch_both(stmt)
    sendMail(emails,title+"\n"+description)



