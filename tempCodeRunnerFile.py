def send_rent_due_email(customer):
    msg = Message('Rent Due Reminder', sender='kun405222@gmail.com', recipients=['elitejhn5@gmail.com'])
    msg.body = f"Rent for {customer.name} is due."
    mail.send(msg)