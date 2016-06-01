""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()
    def create_user(self, info):
        # We write our validations in model functions.
        # They will look similar to those we wrote in Flask
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        # Some basic validation
        if not info['name']:
            errors.append('First Name cannot be blank')

        elif len(info['name']) < 2:
            errors.append('First Name must be at least 2 characters long')

        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:

            return {"status": False, "errors": errors}
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])

            query="INSERT INTO users(name, username, password) VALUES (:name, :email, :password)"
            data={'name':info['name'], 'email':info['email'],'password':pw_hash}

            self.db.query_db(query, data)

            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)

            status = { "status": True, "user": users[0]}
            return status

    def login(self, info):

        errors = []

        query_login = "SELECT * FROM users WHERE username = :email LIMIT 1"
        data = { 'email': info['email'] }
        pw=info['password']
        print "password is", pw

        user = self.db.query_db(query_login, data)
        if user == []:
            print "no user"
            errors.append('InValid1 login!')
            return{"status": False, "errors": errors}
        else:
            if self.bcrypt.check_password_hash(user[0]['password'], info['password']):
                print "password matched"
                return {"status": True, "user": user[0] }
            else:
                print "password not matched"
                errors.append('Invalid login!')
                return{"status": False, "errors": errors}

    def create_item(self, info):
        query="INSERT INTO items (item_name, added_by, created_at)VALUES(:item, :added_by, NOW())"
        data={
        'item':info['item'],
        'added_by':info['added_by'],
        }
        item_id=self.db.query_db(query, data)

        query2="INSERT INTO wishlist (user_id, item_id)VALUES(:user_id, :item_id)"
        data2={'item_id':item_id,
        'user_id':info['added_by']}
        return self.db.query_db(query2, data2)
        return item_id
    def get_items(self, info):
        query="SELECT items.item_name as item, users.name as name,items.created_at as created_at FROM items JOIN wishlist ON items.id=wishlist.item_id JOIN users ON users.id=items.added_by WHERE NOT wishlist.user_id=:id"
        data={'id':info['added_by']}
        return self.db.query_db(query, data)
    def get_my_items(self, info):
        query="SELECT * FROM items WHERE added_by=:added_by"
        data={'added_by':info['added_by']}
        return self.db.query_db(query, data)
    def delete_item(self, info):
        query="DELETE FROM items WHERE id=:id"
        data={'id':info['id']}
        return self.db.query_db(query, data)
    def add_wish_items(self, info2):
        query="INSERT INTO wishlist (user_id, item_id)VALUES(:user_id, :item_id)"
        data={
        'item_id':info2['item_id'],
        'user_id':info2['user_id'],
        }
        return self.db.query_db(query, data)
    def get_wish_items(self, info):
        query="select items.item_name as item_name,items.id as id, users.name as name,items.created_at from items JOIN wishlist ON items.id=wishlist.item_id JOIN users ON items.added_by=users.id Where items.id=:id"
        data={'id':info['id']}
        return self.db.query_db(query, data)
    def rm_wish_list(self,info):
        query="DELETE FROM wishlist WHERE item_id=:id"
        data={'id':info['item_id']}
        return self.db.query_db(query, data)




