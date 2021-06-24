from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_poke import Poke
from flask_app.models.model_user import User

@app.route('/post/new')
def post_new():
    context = {
        'user' : User.get_one(session['uuid'])[0]
    }
    return render_template('new_post.html', **context)

@app.route('/post/create', methods=['POST'])
def post_create():
    is_valid = Poke.validate_post(request.form)
    if not is_valid:
        return redirect('/post/create')
    info = {
        **request.form,
        'user_id' : session['uuid']
    }
    Poke.create(info)
    return redirect('/')

@app.route('/post/<int:post_id>/delete')
def post_delete(post_id):
    post = Poke.get_one(post_id)
    if post['users_id'] == session['uuid']:
        Poke.delete_one(post_id)
    return redirect('/')

@app.route('/post/<int:post_id>/edit')
def edit_post(post_id):
    post_id = Poke.get_one(post_id)
    context = {
        "post" : post_id,
        "user" : session['uuid']
    }
    return render_template('edit_post.html', **context)

@app.route('/post/<int:post_id>/update', methods=['POST'])
def update_post(post_id):
    is_valid = Poke.validate_post(request.form)
    if not is_valid:
        return redirect('/post/<int:post_id>/edit')
    info = {
        "location": request.form['location'],
        "date": request.form['date'],
        "content": request.form['content'],
        "num_of_sas": request.form['num_of_sas'],
        "id" : post_id
    }
    Poke.update_one(info)
    url = f'/post/{post_id}/edit'
    return redirect(url)

@app.route('/post/<int:post_id>/view')
def view_post(post_id):
    post_id = Poke.get_one(post_id)
    user_name = Poke.get_name_by_post(post_id['users_id'])[0]
    context = { 
        "post" : post_id,
        "user_name" : user_name
    }
    return render_template('view_post.html', **context)