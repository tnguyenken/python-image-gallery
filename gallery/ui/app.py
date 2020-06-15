from flask import Flask, flash, request, render_template, redirect, url_for
from db_package import db
import psycopg2

app = Flask(__name__)
app.secret_key = 'dev'

@app.route('/admin')
def users():
    db.connect()
    usernames = db.list_users()
    db.connection.close()
    return render_template('admin.html', users=usernames)

@app.route('/admin/addUser', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']

        db.connect()
        error = None 
        if not user:
            return 'Please enter a username'
        elif not password:
            return 'Please enter a password'
        elif not full_name:
            return 'Please enter a full name'

        if error is None:
            try:
                db.add_user(user, password, full_name)
                return 'You have successfully added the user to your database'
            except psycopg2.errors.UniqueViolation as e:
                return 'The user ' + str(user) + ' already exists'

        db.connection.close()
    return render_template('addUser.html')

@app.route('/admin/deleteUser/<personsName>', methods=['GET', 'POST'])
def deleteUser(personsName):
    if request.method == 'POST':
        confirm = request.form['confirm']

        db.connect()
        db.delete_user(personsName, confirm)
        db.connection.close()
        if confirm:
            return 'You have successfully deleted the user: ' + personsName
        else:
            return 'You have decided not to delete user: ' + personsName

@app.route('/admin/modifyUser/<personsName>', methods=['GET', 'POST'])
def modifyUser(personsName):
    if request.method == 'POST':
        password = request.form['password']
        full_name = request.form['full_name']

        db.connect()
        db.edit_user(personsName, password, full_name)
        db.connection.close()
        return 'You have successfully modified your info for ' + personsName
    return render_template('modifyUser.html', user=personsName)
