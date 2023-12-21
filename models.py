

from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, json
import pickle
import csv


models= Blueprint('models', __name__)
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
    def __init__(self):
        self._observers = []
        self.medicine_details = MedicineDetails()

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, medicine_name):
        if medicine_name[-1] == '1':
            s1.update()
        elif medicine_name[-1] == '2':
            s2.update()

    def run_inventory_check(self):
        self.medicine_details.check_stock_and_notify('pcml1', 'quantity')

class MedicineDetails:
    def __init__(self):
        self.medicines_list = {}

    def display_details(self):
        print(self.medicines_list)
        return self.medicines_list

    def add_medicines(self, medicine_name, quantity, price):
        if medicine_name in self.medicines_list:
            self.medicines_list[medicine_name]['quantity'] += quantity
            self.medicines_list[medicine_name]['price'] = price
            with open("med.pkl", 'wb') as file:
                pickle.dump(self.medicines_list, file)
        else:
            self.medicines_list[medicine_name] = {'quantity': quantity, 'price': price}
            with open("med.pkl", 'ab') as file:
                pickle.dump(self.medicines_list, file)

        with open("med.pkl", 'ab') as file:
            pickle.dump(self.medicines_list, file)

        print(f"MedicineDetails: Adding {quantity} units of {medicine_name} to the inventory.")
        self.check_stock_and_notify(medicine_name, quantity)

    def check_stock_and_notify(self, medicine_name, quantity):
        if medicine_name in self.medicines_list and self.medicines_list[medicine_name]['quantity'] < 20:
            print(f"Alert: Stock of {medicine_name} is below 20. Notifying suppliers.")
            InventoryManager().notify_observers(medicine_name)

    def update_quantities_from_csv(self, csv_file_path):
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)

            # Determine the number of headers
            header_count = len(csv_reader.fieldnames)

            # Skip the header lines
            for _ in range(header_count):
                next(csv_reader)

            # Read and process the CSV data
            csv_dict = {}
            for row in csv_reader:
                medicine_name = row.get("Medicine")
                if medicine_name:
                    csv_quantity = int(row.get("Quantity", 0))
                    csv_dict[medicine_name] = csv_quantity

            # Update medicine quantities
            for medicine_name, csv_quantity in csv_dict.items():
                if medicine_name in self.medicines_list:
                    current_quantity = self.medicines_list[medicine_name]['quantity']

                    # Only update if the new quantity is less than or equal to the current quantity
                    if csv_quantity <= current_quantity:
                        self.medicines_list[medicine_name]['quantity'] -= csv_quantity
                    else:
                        print(f"MedicineDetails: Insufficient quantity of {medicine_name} in the inventory.")
                else:
                    print(f"MedicineDetails: Ignoring {medicine_name} as it is not found in the inventory.")

        # Return the updated medicine list
        return self.medicines_list

class Suppliers:
    def __init__(self, id,obj):
        self.supplier_id = id
        self.obj=obj
    def update(self):
        print(f'Supplier {self.supplier_id}: This medicine is about to expire, so I need more medicines.')
    def add_medicines(self, medicine_name, quantity,price):
        self.obj.add_medicines(medicine_name, quantity,price)

medicinedet = MedicineDetails()
s1=Suppliers(1,medicinedet)

a=InventoryManager()
a.add_observer(s1)
s2=Suppliers(2,medicinedet)
s1.add_medicines("Medicine 10",150,4.5)
s1.add_medicines("Medicine 9",120,4.5)
s1.add_medicines("Medicine 9",120,4.5)
a.add_observer(s2)
a.run_inventory_check()

csv_file_path = 'D:\Design Patterns Project\website\order_history .csv'
medicinedet.update_quantities_from_csv(csv_file_path)

@models.route('/cart')
def cart():
    # Load or generate your medicinesData dictionary
    medicinesData=medicinedet.update_quantities_from_csv("D:\Design Patterns Project\website\order_history .csv")


    print(medicinesData)

    # Render the template and pass the JSON string of medicinesData
    return render_template('cart.html', medicinesData=medicinesData)
