import json
from flask import Flask, jsonify, request,Blueprint,render_template
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

sales= Blueprint('sales', __name__)

with open('sales_data.json') as f:
    sales_data = json.load(f)

# Strategy pattern
class SalesReportStrategy(ABC):
    @abstractmethod
    def generate_report(self, **kwargs):
        pass

class DailySalesReport(SalesReportStrategy):
    def generate_report(self, selected_date):
        for sale in sales_data['sales']:
            if sale['date'] == selected_date:
                date = sale['date']
                medicines_sold = sale['medicines_sold']
                total_sales = sale['total_sales']

                # Find the medicine sold the most
                top_selling_medicine = max(medicines_sold, key=lambda x: x['quantity'])

                report = {
                    "Date": date,
                    "Top Selling Medicine": top_selling_medicine['name'],
                    "Total Sales": total_sales
                }

                return report
        return {"error": "No data found for the given date"}

class WeeklySalesReport(SalesReportStrategy):
    def generate_report(self,start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        weekly_sales = [sale for sale in sales_data['sales'] if start_date <= datetime.strptime(sale['date'], '%Y-%m-%d') <= end_date]

        if weekly_sales:
            total_sales = sum(sale['total_sales'] for sale in weekly_sales)
            medicines_sold = [medicine for sale in weekly_sales for medicine in sale['medicines_sold']]
            medicine_dict = {}

            for medicine in medicines_sold:
                name = medicine['name']
                if name in medicine_dict:
                    medicine_dict[name] += medicine['quantity']
                else:
                    medicine_dict[name] = medicine['quantity']

            top_selling_medicine = max(medicine_dict, key=medicine_dict.get)

            report = {
                "Date Range": {
                    "Start Date": start_date.strftime('%Y-%m-%d'),
                    "End Date": end_date.strftime('%Y-%m-%d')
                },
                "Top Selling Medicine": top_selling_medicine,
                "Total Sales": total_sales
            }

            return report
        else:
            return {"error": "No data found for the given date range"}

class MonthlySalesReport(SalesReportStrategy):
    def generate_report(self, selected_month):
        sales_in_selected_month = []
        for sale in sales_data['sales']:
            sale_date = datetime.strptime(sale['date'], '%Y-%m-%d')
            if sale_date.strftime('%Y-%m') == selected_month:
                sales_in_selected_month.append(sale)

        if sales_in_selected_month:
            total_sales = sum(sale['total_sales'] for sale in sales_in_selected_month)
            medicines_sold = [medicine for sale in sales_in_selected_month for medicine in sale['medicines_sold']]
            medicine_dict = {}

            for medicine in medicines_sold:
                name = medicine['name']
                if name in medicine_dict:
                    medicine_dict[name] += medicine['quantity']
                else:
                    medicine_dict[name] = medicine['quantity']

            top_selling_medicine = max(medicine_dict, key=medicine_dict.get)

            report = {
                "Month": datetime.strptime(selected_month, '%Y-%m').strftime('%B, %Y'),
                "Top Selling Medicine": top_selling_medicine,
                "Total Sales": total_sales
            }

            return report
        else:
            return {"error": "No data found for the given month"}

class AnnualSalesReport(SalesReportStrategy):
    def generate_report(self, selected_year):
        sales_in_selected_year = []
        for sale in sales_data['sales']:
            sale_date = datetime.strptime(sale['date'], '%Y-%m-%d')
            if sale_date.strftime('%Y') == selected_year:
                sales_in_selected_year.append(sale)

        if sales_in_selected_year:
            total_sales = sum(sale['total_sales'] for sale in sales_in_selected_year)
            medicines_sold = [medicine for sale in sales_in_selected_year for medicine in sale['medicines_sold']]
            medicine_dict = {}

            for medicine in medicines_sold:
                name = medicine['name']
                if name in medicine_dict:
                    medicine_dict[name] += medicine['quantity']
                else:
                    medicine_dict[name] = medicine['quantity']

            top_selling_medicine = max(medicine_dict, key=medicine_dict.get)

            report = {
                "Year": selected_year,
                "Top Selling Medicine": top_selling_medicine,
                "Total Sales": total_sales
            }

            return report
        else:
            return {"error": "No data found for the given year"}

class SalesReportContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute_report_generation(self, **kwargs):
        return self.strategy.generate_report(**kwargs)
    
@sales.route('/daily_report')
def daily_report():
   return render_template('daily_report.html')

@sales.route('/weekly_report')
def weekly_report():
   return render_template('weekly_report.html')

@sales.route('/monthly_report')
def monthly_report():
   return render_template('monthly_report.html')

@sales.route('/annual_report')
def annual_report():
   return render_template('annual_report.html')


# Flask routes for fetching reports
@sales.route('/daily_report_form',methods=['GET','POST'])
def daily_report_form():
    if request.method == 'POST':
        selected_date = request.form.get("date")

        if selected_date:
            strategy = DailySalesReport()
            context = SalesReportContext(strategy)
            report = context.execute_report_generation(selected_date=selected_date)
            return render_template('daily_report_result.html', report=report)
        else:
            return jsonify({"error": "Please provide a valid date"}), 400
    else:
        return render_template('daily_report.html')

@sales.route('/weekly_report_form',methods=['GET','POST'])
def weekly_report_form():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if start_date and end_date:
            strategy = WeeklySalesReport()
            context = SalesReportContext(strategy)
            report = context.execute_report_generation(start_date=start_date, end_date=end_date)
            return render_template('weekly_report_result.html', report=report)
        else:
            return jsonify({"error": "Please provide valid start and end dates"}), 400
    else:
        return render_template('weekly_report_form.html')

@sales.route('/monthly_report_form',methods=['GET','POST'])
def monthly_report_form():
    if request.method == 'POST':
        selected_month = request.form.get('month')

        if selected_month:
            strategy = MonthlySalesReport()
            context = SalesReportContext(strategy)
            report = context.execute_report_generation(selected_month = selected_month)
            return render_template('monthly_report_result.html', report=report)
        else:
            return jsonify({"error": "Please provide a valid month (YYYY-MM)"}), 400
    else:
        return render_template('monthly_report_form.html')

@sales.route('/annual_report_form',methods=['GET','POST'])
def annual_report_form():
    if request.method == 'POST':
        selected_year = request.form.get('year')

        if selected_year:
            strategy = AnnualSalesReport()
            context = SalesReportContext(strategy)
            report = context.execute_report_generation(selected_year = selected_year)
            return render_template('annual_report_result.html', report=report)
        else:
            return jsonify({"error": "Please provide a valid year (YYYY)"}), 400
    else:
        return render_template('annual_report_form.html')
