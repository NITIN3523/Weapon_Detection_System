import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer

# Email details
sender_email = 'vp35233523@gmail.com'
receiver_email = None
password = 'cewb vhqq crnu pbpd'  # Be cautious when using hardcoded credentials

# Create a URLSafeTimedSerializer for generating and verifying tokens
secret_key = 'secret_key'
s = URLSafeTimedSerializer(secret_key)

# Function to send detection alert email with tokenized link
def send_detection_link(email):
    # Generate token using email
    token = s.dumps(email, salt='login-page-salt')
    
    # Create the reset URL with the token
    reset_url = f"http://127.0.0.1:5000/?token={token}"
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Weapon Detection Alert'
    
    # Email body with the link
    body = f'Weapon detection alert! To see images, click on this link: {reset_url}'
    msg.attach(MIMEText(body, 'plain'))
    
    # SMTP server setup
    smtp_server = 'smtp.gmail.com'
    port = 587

    try:
        # Connect to the server and start TLS
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()

        # Login to your email account
        server.login(sender_email, password)

        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        print(f'Email sent to {email} with link: {reset_url}')

    except Exception as e:
        print(f'Error: {e}')

    finally:
        server.quit()

# Example: Sending an email
# send_detection_link(receiver_email)
