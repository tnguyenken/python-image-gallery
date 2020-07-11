from flask import Flask, redirect, request, render_template, session

import urllib.parse
from functools import wraps

import boto3
import botocore
from ..data.user import User
from ..data.postgres_user_dao import PostgresUserDAO
from ..data.db import connect
from ..aws.secrets import get_secret_flask_session
from ..aws.s3 import create_bucket
from ..upload.file_upload import upload_file

s3 = boto3.resource('s3')
app = Flask(__name__)
app.secret_key = get_secret_flask_session()

S3_IMAGE_BUCKET = 'edu.au.cc.image-gallery26'
my_region = 'us-east-1'


# Database connection
connect()

def get_user_dao():
    return PostgresUserDAO()

def check_admin():
    return 'username' in session and session['username'] == 'fred'

def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        return view(**kwargs)
    return decorated

def check_user():
    users=get_user_dao().get_users()
    for user in users:
        if 'username' in session and session['username'] == user._User__username:
            return True
    return False

def requires_user(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_user():
            return redirect('/login')
        return view(**kwargs)
    return decorated


def bucket_exists(users_bucket_name):
    bucket = s3.Bucket(S3_IMAGE_BUCKET+'/'+users_bucket_name)
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket='mybucket')
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False
        
@app.route('/')
@requires_user
def main_menu():
    if check_admin():
        return render_template('main_admin.html', username=str(session['username']))
    return render_template('main_user.html', username=str(session['username']))

@app.route('/upload_file/<username>', methods=['GET', 'POST'])
@requires_user
def upload_images(username):
    if bucket_exists(str(session['username'])) == False:
        create_bucket(bucket_name=S3_IMAGE_BUCKET+'.'+str(session['username']), region=my_region)
    upload_file(str(session['username']))
    return render_template('upload_form.html')

@app.route('/invalidLogin')
def invalidLogin():
    return "Invalid"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_dao().get_user_by_username(request.form["username"])
        if user is None or user._User__password != request.form["password"]:
            return redirect('/invalidLogin')
        else:
            session['username'] = request.form["username"]
            return redirect("/")
    else:
        return render_template('login.html')

@app.route('/debugSession')
def debugSession():
    result = ""
    for key,value in session.items():
        result += key+"->"+str(value)+"<br />"
    return result

@app.route('/admin/executeAddUser')
@requires_admin
def execute_add_user(username, password, full_name):
    get_user_dao().add_user(username, password, full_name)

@app.route('/admin/addUser', methods=['GET', 'POST'])
@requires_admin
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        execute_add_user(username, password, full_name)
        return redirect('/admin/users')
    return render_template('add_user.html')

@app.route('/admin/executeEditUser/<username>')
@requires_admin
def execute_edit_user(username, password, full_name):
    get_user_dao().edit_user(username, password, full_name)

@app.route('/admin/editUser/<username>', methods=['GET', 'POST'])
@requires_admin
def edit_user(username):
    if request.method == 'POST':
        password = request.form['password']
        full_name = request.form['full_name']
        execute_edit_user(username, password, full_name)
        return redirect('/admin/users')
    return render_template('edit_user.html', username=username)

@app.route('/admin/executeDeleteUser/<username>')
@requires_admin
def execute_delete_user(username):
    get_user_dao().delete_user(username)
    return redirect('/admin/users')

@app.route('/admin/deleteUser/<username>')
@requires_admin
def delete_user(username):
    return render_template('confirm.html',
                           title='Confirm delete',
                           message='Are you sure you want to delete this user',
                           on_yes='/admin/executeDeleteUser/' + urllib.parse.quote(username),
                           on_no='/admin/users')

@app.route('/admin/users')
@requires_admin
def users():
    return render_template('users.html', users=get_user_dao().get_users())
