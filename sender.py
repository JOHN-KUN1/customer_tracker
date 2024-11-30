from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from app import app,db,Customer
from datetime import datetime, timedelta

mail = Mail(app)


with app.app_context():
    db.create_all()

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'olivehousing2@gmail.com'
app.config['MAIL_PASSWORD'] = 'rzff cjry rivu doyq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

def send_rent_due_email(customer):
    msg = Message('Rent Due Reminder', sender='olivehousing2@gmail.com', recipients=['elitejhn5@gmail.com'])
    msg.body = f"Rent for {customer.name} is due."
    mail.send(msg)

def rent_due_checker():
    with app.app_context():
        now = datetime.now()
        customers = Customer.query.all()
        for customer in customers:
            if now >= customer.date_due:
                print(f"now: {now}, customerDate : {customer.date_due + timedelta(minutes=1)}")
                send_rent_due_email(customer)
                print("sent")
                db.session.delete(customer)
                db.session.commit()

if __name__ == '__main__': 
    rent_due_checker()