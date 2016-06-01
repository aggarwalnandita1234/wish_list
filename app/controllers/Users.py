"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *


class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        session['key']='os.urandom(n)'
        self.load_model('User')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('index.html')
    def dashboard(self):
        info={'added_by':session['id']}
        items=self.models['User'].get_items(info)
        print "These are items", items

        items2=self.models['User'].get_my_items(info)
        info2={'id':session['id']}
        get_wish_items=self.models['User'].get_wish_items(info2)
        print "This is", get_wish_items
        return self.load_view('dashboard.html', items=items, items2=items2, wish_items=get_wish_items)
    def add_item(self):
        return self.load_view('add_item.html')
    def wish_items(self):
        return self.load_view('wish_items.html')
    def logout(self):
        session.clear()
        return redirect('/')

    def create(self):

        info = {
             "name" : request.form['form-first-name'],
             "email": request.form['form-email'],
             "password":request.form['form-password'],
             "pw_confirmation" : request.form['form-conf-password']
        }
        create_status = self.models['User'].create_user(info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['name'] = create_status['user']['name']

            return redirect('/dashboard')
        else:

            for message in create_status['errors']:
                flash(message, 'regis_errors')

            return redirect('/')

    def login(self):
        info = {
            "email" : request.form['form-email'],
            "password" : request.form['form-password']
        }        
        create_status = self.models['User'].login(info)
        if create_status['status'] == True:
            print "we are in create_status=True"
            session['id'] = create_status['user']['id']
            session['name'] = create_status['user']['name']          
            return redirect('/dashboard')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def create_item(self):
        info={
        'item':request.form['item'],
        'added_by':session['id']
        }
        item_id= self.models['User'].create_item(info)
        return redirect('/dashboard')
    def delete(self, id):
        info={'id':id}
        self.models['User'].delete_item(info)
        return redirect('/dashboard')
    def wish_items(self, id):
        info2={
        'item_id': id,
        'user_id':session['id']
        }
        wish_items=self.models['User'].add_wish_items(info2)
        return redirect('/dashboard')
    def rm_wish_list(self, id):
        info={'item_id': id}   
        self.models['User'].rm_wish_list(info)  
        return redirect('/dashboard')   




