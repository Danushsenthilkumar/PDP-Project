from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, json
import pickle
import csv
import json
import os
from datetime import date,timedelta

models = Blueprint('models', __name__)
class User:
    def __init__(self, name, age, address, email, password, username, district, state, pin, accountholder, accountnumber, upiid, gpaynumber):
        self.name = name
        self.age = age
        self.address = address
        self.email = email
        self.password = password
        self.username = username
        self.district = district
        self.state = state
        self.pin = pin
        self.accountholder = accountholder
        self.accountnumber = accountnumber
        self.upiid = upiid
        self.gpaynumber = gpaynumber
class InventoryManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryManager, cls).__new__(cls)
            cls._instance._observers = []
            cls._instance.medicine_details = MedicineDetails()
        return cls._instance
    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, medicine_name):
        for observer in self._observers:
            if medicine_name in observer.medicines_supplied:
                observer.update()

    def run_inventory_check(self):
        self.medicine_details.check_stock_and_notify('pcml1', 'quantity')

class MedicineDetails:
    def __init__(self):
        self.medicines_list={}
    def add_medicines(self, medicine_name, quantity, price, expiry_date):
        if medicine_name in self.medicines_list:
            self.medicines_list[medicine_name]['quantity'] += quantity
            self.medicines_list[medicine_name]['price'] = price
            self.medicines_list[medicine_name]['expiry_date'] = expiry_date
        else:
            self.medicines_list[medicine_name] = {'quantity': quantity, 'price': price, 'expiry_date': expiry_date}
        
        self.check_stock_and_notify(medicine_name, quantity)
    def update_details(self, updated_details=None):
        if updated_details is not None:
            self.medicines_list.update(updated_details)
            with open("med.json", 'w') as file:
                json.dump(self.medicines_list, file, default=str)
            return self.medicines_list
        else:
            return self.medicines_list
    

    def check_stock_and_notify(self, medicine_name, quantity):
        if medicine_name in self.medicines_list and self.medicines_list[medicine_name]['quantity'] < 20:
            print(f"Alert: Stock of {medicine_name} is below 20. Notifying suppliers.")
            InventoryManager().notify_observers(medicine_name)

class Suppliers:
    def __init__(self, id, obj, medicines_supplied):
        self.supplier_id = id
        self.obj = obj
        self.medicines_supplied = medicines_supplied
    def update(self):
        print(f'Supplier {self.supplier_id}: One of the supplied medicines is about to expire, so I need more medicines.')
    def add_medicines(self, medicine_name, quantity, price, expiry_date):
        self.obj.add_medicines(medicine_name, quantity, price, expiry_date)
medicinedet = MedicineDetails()
s1 = Suppliers(1, medicinedet, ["Medicine10","Medicine9"])
a = InventoryManager()
a.add_observer(s1)
s2 = Suppliers(2, medicinedet, ["Medicine6","Medicine4"])
s1.add_medicines("Medicine10",150, 4.5, date(2023, 12, 23))
s1.add_medicines("Medicine9",120, 4.5, date(2023, 11, 25))
s1.add_medicines("Medicine9",120, 4.5, date(2023, 10, 25))
s2.add_medicines("Medicine6",130, 5, date(2023, 9, 25))
s2.add_medicines("Medicine4",130, 5, date(2023, 8, 25))
a.add_observer(s2)
a.run_inventory_check()


@models.route('/cart')
def cart():
   medicinesData=medicinedet.medicines_list
   return render_template('cart.html', medicinesData=medicinesData)
class MedicineState:
    def execute(self):
        pass
class NormalState(MedicineState):
    def execute(self):
        status='The Medicine is in Normal State'
        return status
class AboutToExpireState(MedicineState):
    def execute(self):
        status='The Medicine is About To Expire'
        return status
class ExpiredState(MedicineState):
    def execute(self):
        status='The Medicine is Already Expired'
        return status
class StateDecider():
    def __init__(self):
        self.state=None

    def set_state(self,state):
        self.state=state

    def execution(self):
        return self.state.execute()
@models.route('/expirychecker',methods=['GET','POST'])
def expirychecker():
    if request.method=='POST':
        medicine_name=request.form.get('medicineName')
        medicine_list = medicinedet.medicines_list
        state=StateDecider()
        normal=NormalState()
        aboutToExpire=AboutToExpireState()
        expired=ExpiredState()
        if medicine_name in medicine_list:
            expiry_date=medicine_list[medicine_name]['expiry_date']
            day_difference=expiry_date-date.today()
            print(day_difference)
            if day_difference.days>30:
                state.set_state(normal)
                status=state.execution()
                return render_template('expiration.html', report=status)
            elif day_difference.days>0 and day_difference.days<30:
                state.set_state(aboutToExpire)
                status=state.execution()
                return render_template('expiration.html', report=status)
            else:
                state.set_state(expired)
                status=state.execution()
                return render_template('expiration.html', report=status)
        else:
            status='Sorry the medicine is not Available'
            return render_template('expiration.html', report=status)
    else:
        return render_template('expiration.html')
def update_quantities_from_csv(csv_file_path,new_csv, medicines_list=None):
    if os.path.getsize("med.json")==0:
        medicines_list=medicinedet.medicines_list
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file, quotechar='"')
            csv_dict = {}
            for index, row in enumerate(csv_reader):
                medicine_name = row.get("Medicine")
                if medicine_name:
                    csv_quantity = int(row.get("Quantity", 0))
                    csv_dict[medicine_name] = csv_quantity

            for medicine_name,csv_quantity in csv_dict.items():
                if medicine_name in medicines_list:
                    current_quantity = medicines_list[medicine_name]['quantity']
                    if csv_quantity <= current_quantity:
                        medicines_list[medicine_name]['quantity'] -= csv_quantity
                        medicines_list = medicinedet.update_details(medicines_list)
                    else:
                        print(f"MedicineDetails: Insufficient quantity of {medicine_name} in the inventory.")
                else:
                    print(f"MedicineDetails: Ignoring {medicine_name} as it is not found in the inventory.")
        clear_input_file_content(csv_file_path,new_csv)
        return medicines_list
    else:
        with open('med.json', 'r') as file:
            medicines_list = json.load(file)
           
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file, quotechar='"')
            csv_dict = {}
            for index, row in enumerate(csv_reader):
                medicine_name = row.get("Medicine")
                if medicine_name:
                    csv_quantity = int(row.get("Quantity", 0))
                    csv_dict[medicine_name] = csv_quantity
        
            for medicine_name,csv_quantity in csv_dict.items():
                if medicine_name in medicines_list:
                    current_quantity = medicines_list[medicine_name]['quantity']
                    if csv_quantity <= current_quantity:
                        medicines_list[medicine_name]['quantity'] -= csv_quantity
                        medicines_list = medicinedet.update_details(medicines_list)
                    else:
                        print(f"MedicineDetails: Insufficient quantity of {medicine_name} in the inventory.")
                else:
                    print(f"MedicineDetails: Ignoring {medicine_name} as it is not found in the inventory.")
        clear_input_file_content(csv_file_path,new_csv)
        return medicines_list
def clear_input_file_content(old_csv,new_csv):
    with open(old_csv, "r") as input_file:
        csv_reader = csv.reader(input_file)
        data_to_append = list(csv_reader)
    with open(new_csv, "a", newline="") as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerows(data_to_append)
    with open(old_csv, "w", newline="") as input_file:
        input_file.truncate(0)