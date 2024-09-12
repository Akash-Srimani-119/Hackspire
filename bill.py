import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def generate_bill():
    customer_name = "John Doe"
    items = [
        {"name": "Apples", "quantity": 3, "price": 0.5},
        {"name": "Bananas", "quantity": 2, "price": 0.3},
        {"name": "Milk", "quantity": 1, "price": 1.2},
    ]
    
    total = sum(item['quantity'] * item['price'] for item in items)

    bill = f"Bill for {customer_name}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    bill += f"{'Item':<20}{'Quantity':<10}{'Price':<10}{'Total':<10}\n"
    bill += "-"*50 + "\n"
    for item in items:
        item_total = item['quantity'] * item['price']
        bill += f"{item['name']:<20}{item['quantity']:<10}{item['price']:<10}{item_total:<10}\n"
    bill += "-"*50 + "\n"
    bill += f"{'Total':<40}{total:<10}\n"

    return bill

def send_email(bill, recipient_email):
    sender_email = "from@example.com"  # Replace with your Mailtrap sender email
    receiver_email = recipient_email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Your Bill"

    msg.attach(MIMEText(bill, 'plain'))

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login("c4d7746035d322", "bdd4bfdb4cc2c2")
        server.send_message(msg)
        print("Email sent successfully!")

if __name__ == "__main__":
    bill = generate_bill()
    print(bill)
    send_email(bill, "sky119akash@gmail.com")
