import smtplib
from email.mime.text import MIMEText

sender_email = "sreenandhpreneeshtp@gmail.com"
app_password = "oity fict acnt qwwb"

receiver_email = "sreenandhpreneesh19@gmail.com"

msg = MIMEText("This is a test email")
msg["Subject"] = "Email Test"
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)

    print("Connected")

    server.starttls()

    print("TLS Started")

    server.login(sender_email, app_password)

    print("Login Successful")

    server.sendmail(
        sender_email,
        receiver_email,
        msg.as_string()
    )

    print("Email Sent Successfully")

    server.quit()

except Exception as e:
    print("ERROR:", e)