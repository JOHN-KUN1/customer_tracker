import multiprocessing.process
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import threading
import multiprocessing

app = Flask(__name__)

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kun405222@gmail.com'
app.config['MAIL_PASSWORD'] = 'hezx ohvj lhry topt'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Define Customer Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    house_number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    plot_number = db.Column(db.String(50), nullable=False)
    meter_number = db.Column(db.String(50), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)
    maintainance = db.Column(db.String(200), nullable=False)
    service_charge = db.Column(db.String(200), nullable=False)
 
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        customer = Customer(
            description=request.form['description'],
            house_number=request.form['house_number'],
            name=request.form['name'],
            plot_number=request.form['plot_number'],
            meter_number=request.form['meter_number'],
            entry_date=datetime.strptime(request.form['entry_date'], '%Y-%m-%d'),
            maintainance=request.form['maintainance'],
            service_charge=request.form['service_charge']
        )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('index'))

    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/delete', methods=['POST'])
def delete_customer():
    customer_id = int(request.form['customer_id'])
    customer = Customer.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('index'))

def send_rent_due_email(customer):
    msg = Message('Rent Due Reminder', sender='kun405222@gmail.com', recipients=['elitejhn5@gmail.com'])
    msg.body = f"Rent for {customer.name} is due."
    mail.send(msg)

def rent_due_checker():
    with app.app_context():
        while True:
            now = datetime.now()
            customers = Customer.query.all()
            for customer in customers:
                if now >= customer.entry_date + timedelta(minutes=1):
                    send_rent_due_email(customer)
                    print("sent")
                    db.session.delete(customer)
                    db.session.commit()
            multiprocessing.Event().wait(60)  # Check once every minute


if __name__ == '__main__':
    multiprocessing.Process(target=rent_due_checker).start()
    app.run(debug=True)
