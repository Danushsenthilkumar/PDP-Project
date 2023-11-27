from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
import pickle

class User:
    def __init__(self,name,age,address,email,password,username,district,state,pin,accountholder,accountnumber,upiid,gpaynumber):
        self.name=name
        self.age=age
        self.address=address
        self.email=email
        self.password=password
        self.username=username
        self.district=district
        self.state=state
        self.pin=pin
        self.accountholder=accountholder
        self.accountnumber=accountnumber
        self.upiid=upiid
        self.gpaynumber=gpaynumber
    def save_user_data_to_pickle(self):
        with open("users.pkl", 'wb') as file:
            pickle.dump(self, file)
    def load_user_data_from_pickle(self):     
        try:
            with open("users.pkl", 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}
    


class lpage(db.Model, UserMixin):
    email = db.Column(db.String(150),primary_key=True)
    password = db.Column(db.String(150))

    
