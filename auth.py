from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .models import lpage
from . import db
from werkzeug.security import generate_password_hash, check_password_hash



auth = Blueprint('auth', __name__)



@auth.route('/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new1_user = lpage(password=hash_password,email=email)
        db.session.add(new1_user)
        db.session.commit()
        return redirect(url_for('views.home'))
    else:
        return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return "logged out"

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        age = request.form.get("age")
        address = request.form.get("address")
        email = request.form.get("email")
        password = request.form.get("password")
        username=request.form.get("username")
        district=request.form.get("district")
        state=request.form.get("state")
        pin=request.form.get("pin")
        accountholder=request.form.get("accountholder")
        accountnumber=request.form.get("accountnumber")
        upiid=request.form.get("upiid")
        gpaynumber=request.form.get("gpaynumber")
        # Use the correct syntax for method parameter
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        userdata=User(name,age,address,email,hashed_password,username,district,state,pin,accountholder,accountnumber,upiid,gpaynumber)
        userdata.save_user_data_to_pickle()
        userdata=userdata.load_user_data_from_pickle()
        return redirect(url_for('auth.login'))
    else:
        return render_template("signup.html", boolean=True)
    
