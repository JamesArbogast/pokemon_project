from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/login')
def login():
    if 'uuid' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/process_login', methods = ['POST'])
def process_login():
    list_of_users = User.get_one_by_email(request.form['email'])
    if len(list_of_users) <= 0:
        print("User doesn't exist")
        return redirect('/login')
    user = list_of_users[0]
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Incorrect Password")
        return redirect('/login')
    session['uuid'] = user['id']
    return redirect('/', user_id = user)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'uuid' in session:
        session.clear()
    return redirect('/')