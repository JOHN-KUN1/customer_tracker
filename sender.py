from flask_mail import Mail, Message
from app import app

mail = Mail(app)

# Define Customer Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    date_due = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200), nullable=False) 
    house_number = db.Column(db.String(50), nullable=False) 
    name = db.Column(db.String(100), nullable=False) 
    plot_number = db.Column(db.String(50), nullable=False) 
    phone_number = db.Column(db.String(50), nullable=False) 
    meter_number = db.Column(db.String(50), nullable=False) 
    maintainance = db.Column(db.String(200), nullable=False) 
    service_charge = db.Column(db.String(200), nullable=False) 
    form_of_identification = db.Column(db.String(200), nullable=False) 
    occupation = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'olivehousing2@gmail.com'
app.config['MAIL_PASSWORD'] = 'rzff cjry rivu doyq'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

def send_rent_due_email(customer):
    msg = Message('Rent Due Reminder', sender='olivehousing2@gmail.com', recipients=['elitejhn5@gmail.com'])
    msg.body = f"Rent for {customer.name} is due."
    mail.send(msg)

def rent_due_checker():
    with app.app_context():
        now = datetime.now()
        customers = Customer.query.all()
        for customer in customers:
            if now >= customer.date_due + timedelta(minutes=1):
                send_rent_due_email(customer)
                print("sent")
                db.session.delete(customer)
                db.session.commit()


if __name__ == '__main__': 
    rent_due_checker()