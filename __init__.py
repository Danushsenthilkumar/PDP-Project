# website/__init__.py

from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail, Message

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = "Danush@#1405"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from.models import models
    from .Prescription_and_sales_history_final import prescription
    from .Sales_hist import sales
    from .stock import stockblueprint
    

    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(models, url_prefix='/')
    app.register_blueprint(prescription, url_prefix='/')
    app.register_blueprint(sales, url_prefix='/')
    app.register_blueprint(stockblueprint, url_prefix='/stocks')
    

    # Configure Flask-Mail for Gmail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'danushsenthil779@gmail.com'
    app.config['MAIL_PASSWORD'] = 'vgnn fokp ueqt vsnu'
    app.config['MAIL_DEFAULT_SENDER']='danushsenthil779@gmail.com'

    mail = Mail(app)

    

    @app.route('/send_email',methods=['GET', 'POST'])
    def send_email():
        if request.method == 'POST':
            recipient_email=request.form.get('email')
            # Create a Flask-Mail message
            msg = Message('Your Desired Subject', recipients=[recipient_email])
            msg.body = 'Please find the attached PDF.'
            # Attach the PDF file (replace with your PDF file path)
            pdf_file_path = r'D:\Design Patterns Project\Medical Shop Cart.pdf'
            with views.open_resource(pdf_file_path) as pdf_file:
                msg.attach('document.pdf', 'application/pdf', pdf_file.read())
            mail.send(msg)
            return 'Email sent successfully!'
            
        else:
            return render_template('bill.html')
    return app