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
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        sql="insert into user(username,usertype,email,password) values(?,?,?,?);"
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
        print("insert into user(username,usertype,email,password) values("+form.username.data+","+form.usertype.data+","+form.email.data+","+hashed_password+");")
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,form.username.data)
        ibm_db.bind_param(stmt,2,form.usertype.data)
        ibm_db.bind_param(stmt,3,form.email.data)
        ibm_db.bind_param(stmt,4,hashed_password)
        ibm_db.execute(stmt)
        flash('You account has been created! You are now able to log in', 'success')
        return redirect(url_for('updateprofile'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = LoginForm()
    if form.validate_on_submit():
        sql="select * from user where email=? limit 1;"
        conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;PROTOCOL=TCPIP;SECURITY=SSL;UID=IBM_UID;PWD=IBM_PID;","","")
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,form.email.data)
        ibm_db.execute(stmt)
        users=ibm_db.fetch_both(stmt)
        user=None
        if users!=False:
            print(users)
            user=User(users[0],users[1],users[2],users[3],users[4])
            print(user.password)
        else:
            flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
            return render_template('login.html', form=form)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print('password clear')
            if form.usertype.data == user.usertype and form.usertype.data == 'Company':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('posted_jobs'))
            elif form.usertype.data == user.usertype and form.usertype.data == 'Job Seeker':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('show_jobs'))
            else:
                flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
        else:
            flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_jobs'))

