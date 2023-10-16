import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

if __name__ == '__main__':
    # Email configuration
    smtp_server = 'localhost'  # Replace with your SMTP server address
    smtp_port = 1025  # Replace with your SMTP server port
    sender_email = 'lahavs512@gmail.com'  # Your email address
    receiver_email = 'lahavs512@gmail.com'  # Recipient's email address

    # Create a message
    subject = 'Hello, Python!'
    message = 'This is a test email sent from Python.'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        # server.starttls()  # Use TLS encryption
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
    finally:
        server.quit()
