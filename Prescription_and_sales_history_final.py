from flask import Flask, jsonify, request, render_template,Blueprint
import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

prescription= Blueprint('prescription', __name__)

class PrescriptionBuilder:
    def __init__(self):
        self.prescription = {
            "patient_name": "",
            "date": "",
            "medicines": [],
            "doctor_name": ""
        }

    def with_patient_details(self, name, date):
        self.prescription["patient_name"] = name
        self.prescription["date"] = date
        return self

    def with_medicine(self, medicine_name, quantity):
        self.prescription["medicines"].append({"medicine_name": medicine_name, "quantity": quantity})
        return self

    def with_doctor_details(self, doctor_name):
        self.prescription["doctor_name"] = doctor_name
        return self

    def build(self):
        return self.prescription

class Medicine:
    def __init__(self, medicine_name, quantity):
        self.medicine_name = medicine_name
        self.quantity = quantity

    def to_dict(self):
        return {
            "medicine_name": self.medicine_name,
            "quantity": self.quantity
        }

def save_to_json(prescription_data):
    
    print(prescription_data)
    with open('prescriptions.json', 'a') as json_file:
        json.dump(prescription_data, json_file)
        json_file.write('\n')
    # Explicitly close and reopen the file
    with open('prescriptions.json', 'a'):
        pass

@prescription.route('/create_prescription', methods=['GET', 'POST'])
def create_prescription():
    if request.method == 'POST':
        data = request.form

        patient_name = data.get('patient_name')
        date = data.get('date')
        medicines_data = zip(data.getlist('medicine_name[]'), data.getlist('quantity[]'))
        doctor_name = data.get('doctor_name')

        prescription_builder = PrescriptionBuilder()
        prescription_builder.with_patient_details(patient_name, date)

        for med_name, quantity in medicines_data:
            prescription_builder.with_medicine(med_name, quantity)

        prescription_builder.with_doctor_details(doctor_name)

        prescription_data = prescription_builder.build()

        
        save_to_json(prescription_data)

        return jsonify({"message": "Prescription created successfully"})

    return render_template('create_prescription.html')
    
    






