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

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):

        return self.load_view('index.html')
    def dashboard(self):
        return self.load_view('dashboard.html')
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

