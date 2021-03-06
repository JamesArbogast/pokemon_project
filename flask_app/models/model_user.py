from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

DATABASE_SCHEMA = 'poke_db'

class User: #pascal case -> first upper, rest lower, word is singular
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#C
    @classmethod
    def create(cls, info):
        query = "INSERT INTO users (username, first_name, last_name, email, pw) VALUES (%(username)s, %(first_name)s, %(last_name)s, %(email)s, %(hash_pw)s)"
        data = {
            "username" : info['username'], 
            "first_name" : info['first_name'],
            "last_name" : info['last_name'],
            "email" :   info['email'],
            "hash_pw" : info['hash_pw']
        }
        new_user_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print(new_user_id)
        return new_user_id

#R
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        all_table_name = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        all_users = []
        for user in all_table_name:
            all_users.append(cls(user))
        return all_table_name

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM users WHERE id= %(user_id)s;"
        data = {
            "user_id": id
        }
        print(data)
        one_table_name = connectToMySQL(DATABASE_SCHEMA).query_db(query, data) 
        print(one_table_name)
        return one_table_name

    @classmethod
    def get_one_by_name(cls, name):
        query = "SELECT * FROM users WHERE name= %(name)s;"
        data = {
            "name": name
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)   
        return result

    @classmethod
    def get_one_by_email(cls, email):
        query = "SELECT * FROM users WHERE email= %(email)s;"
        data = {
            "email": email
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)   
        return result
    
#U
    @classmethod
    def update_one(cls, info):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id=%(id)s;"
        data = {
            "first_name": info['first_name'],
            "last_name": info['last_name'],
            "email": info['email'],     
            "password": info['password'],
            "id": info['id']
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return result
#D
    @classmethod
    def delete_one(cls, id):
        query = "DELETE FROM users WHERE id=%(id)s;"
        data = {
            "id": id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print(f"The user with the ID:{id} has been deleted")
        return id
    
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['username']) < 3:
            flash("USername must be at least 3 characters.")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False    
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(user['email']) < 5:
            flash("Email     must be at least 5 characters")
            is_valid = False
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(user['pw']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['pw'] != user['confirm_pw']:
            flash("Password must match confirmation")
            is_valid = False
        return is_valid