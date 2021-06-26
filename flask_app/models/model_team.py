from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

DATABASE_SCHEMA = 'poke_db'

class Post: #pascal case -> first upper, rest lower, word is singular
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.date = data['date']
        self.content = data['content']
        self.num_of_sas = data['num_of_sas']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id  = data['users_id']   

#C
    @classmethod
    def create(cls, info):
        query = "INSERT INTO posts (location, date, content, num_of_sas, users_id) VALUES (%(location)s, %(date)s, %(content)s, %(num_of_sas)s, %(users_id)s)"
        data = {
            "location" : info['location'],
            "date" : info['date'],
            "content" : info['content'],    
            "num_of_sas" : info['num_of_sas'],
            "users_id" : session['uuid']
        }
        new_user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_user_id

#R
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts"
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        all_posts = []
        for post in results:
            all_posts.append(cls(post))
        return all_posts

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM posts WHERE id= %(id)s;"
        data = {
            "id": id
        }
        one_user = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return one_user[0]

    @classmethod
    def get_one_by_email(cls, email):
        query = "SELECT * FROM posts WHERE email= %(email)s;"
        data = {
            "email": email
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)   
        return result

    @classmethod
    def get_name_by_post(cls, id):
        query = "SELECT first_name, last_name FROM users JOIN posts ON posts.users_id = users.id WHERE posts.users_id = %(id)s;"
        data = {    
            "id" : id
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print("*"*80)
        print(result)   
        print("*"*80)
        return result

#U
    @classmethod
    def update_one(cls, info):
        query = "UPDATE posts SET location=%(location)s, date=%(date)s, content=%(content)s, num_of_sas=%(num_of_sas)s WHERE id=%(id)s;"
        data = {
            "location": info['location'],
            "date": info['date'],
            "content": info['content'],
            "num_of_sas": info['num_of_sas'],
            "id": info['id']
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return result
#D
    @classmethod
    def delete_one(cls, id):
        query = "DELETE FROM posts WHERE id=%(id)s;"
        data = {
            "id": id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return id

    @staticmethod
    def validate_post(post):
        is_valid = True # we assume this is true
        if len(post['location']) < 5:
            flash("Location must be at least 5 characters.")
            is_valid = False
        if len(post['content']) < 5:
            flash("What happened must be at least 5 characters")
            is_valid = False
        if len(post['num_of_sas']) < 1:
            flash("There has to have been at least one sasquatch.")
            is_valid = False
        return is_valid
