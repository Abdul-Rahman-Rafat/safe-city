import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_mail(receiver_mail, image_path , incident_type , location):
    email = 'safecityfcis@gmail.com'
    password = 'jvhqfhhfszbhgtys'
    
    subject = "Incident detected"
    message = (
        "An incident is detected in the system. Please check the alerts section.\n\n"
        f"Type: {incident_type}\n"
        f"Location: {location}"
    )

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = receiver_mail
    msg['Subject'] = subject

   
    msg.attach(MIMEText(message, 'plain'))

    with open(image_path, 'rb') as img:
        mime = MIMEImage(img.read())
        mime.add_header('Content-Disposition', 'attachment', filename=image_path)
        msg.attach(mime)

    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, receiver_mail, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


