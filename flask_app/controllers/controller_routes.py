from flask_app.models.model_poke import Poke
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User

@app.route('/')
def index():
    if 'uuid' not in session:
        return redirect('/login')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/login')
    context = { 
        "user" : User.get_one(session['uuid'])[0],
        #"all_posts" : Poke.get_all()
    }
    print(User.get_one(session['uuid'])[0])
    return render_template('dashboard.html', **context)
