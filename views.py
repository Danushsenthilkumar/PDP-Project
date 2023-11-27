#ANYTHING THAT IS NOT RELATED TO AUTHENTICATION THAT THE USER WANTS TO NAVIGATE IS PUT IN THIS FILE
from flask import Blueprint,render_template

views=Blueprint('views',__name__)



@views.route('/home')
def home():
    return render_template("home.html")



