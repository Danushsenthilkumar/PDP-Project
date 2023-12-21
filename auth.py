from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import sqlite3

from .models import User
auth = Blueprint('auth', __name__)
user_l=[]

mydb = sqlite3.connect("cart.db", check_same_thread=False)
cursor = mydb.cursor()
try:
    cursor.execute("create table cart(medicine_name varchar(100), qty int, price real);")
except sqlite3.OperationalError:
    pass

def load_data():
    try:
        with open("final.pkl", 'rb') as file:
            loaded_data = []
            while True:
                try:
                    item = pickle.load(file)
                    loaded_data.append(item)
                except EOFError:
                    break
            return loaded_data
    except FileNotFoundError:
        return []
    
def save_user_data(data):
    with open("final.pkl", 'ab') as file:
        pickle.dump(data, file)

@auth.route('/', methods=['GET', 'POST'])
def login():
    global user_list
    user_list=load_data()
    print(user_list)
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        for i in user_list:
            for j in i:
                if j.email==email:
                    if check_password_hash(j.password, password):
                        session['cart'] = {}    
                        return redirect(url_for('views.home'))
                    else:
                        flash('Incorrect password. Please try again.')
                        return redirect(url_for('auth.login'))
        return redirect(url_for('auth.signup'))
    else:
        return render_template("login.html", boolean=True)

@auth.route('/logout')
def logout():
    return "logged out"

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    global user_list
    if request.method == 'POST':
        name = request.form.get("name")
        age = request.form.get("age")
        address = request.form.get("address")
        email = request.form.get("email")
        password = request.form.get("password")
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        username = request.form.get("username")
        district = request.form.get("district")
        state = request.form.get("state")
        pin = request.form.get("pin")
        accountholder = request.form.get("accountholder")
        accountnumber = request.form.get("accountnumber")
        upiid = request.form.get("upiid")
        gpaynumber = request.form.get("gpaynumber")
        # Create a new User instance
        new_user = User(
            name, age, address, email, hash_password, username,
            district, state, pin, accountholder, accountnumber, upiid, gpaynumber
        )
        user_l.append(new_user) 
        save_user_data(user_l)
        return redirect(url_for('auth.login'))
    else:
        return render_template("signup.html", boolean=True)
    
@auth.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if request.method == "POST":
        medicine_name = request.form.get("medicine_name")
        qty = int(request.form.get("quantity"))
        amount = float(request.form.get("price")) * qty

        cursor.execute(f"select count(*) from cart where medicine_name='{medicine_name}'")
        res = cursor.fetchone()

        print("Count Result:", res)

        if res != (0,):
            cursor.execute(f'''
                           update cart
                           set qty = qty + {qty}, price = price + {amount}
                           where medicine_name = '{medicine_name}';
                           ''')
        else:
            command = f"insert into cart values ('{medicine_name}', {qty}, {amount});"
            print("Insert Command:", command)
            cursor.execute(command)

        mydb.commit()

        cursor.execute("select * from cart")
        fetched_data = cursor.fetchall()
        print("Fetched Data:", fetched_data)

        return jsonify({"response": "added to cart"})
    else:
        return jsonify({"error": "cannot add to cart"})