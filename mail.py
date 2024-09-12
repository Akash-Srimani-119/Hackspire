import smtplib

sender = "sandbox.smtp.mailtrap.io"
receiver = "sky119akash@gmail.com"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
    server.starttls()
    server.login("c4d7746035d322", "bdd4bfdb4cc2c2")
    server.sendmail(sender, receiver, message)