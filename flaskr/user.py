from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, ID, auth = False):
        self.id = ID
        self.auth = auth
    
    def get_id(self):
        return self.id


