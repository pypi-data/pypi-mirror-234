from email.message import EmailMessage
import smtplib

def send_mail():
    try:
        sender = "carlos.pacheco@kemok.io"
        to = "carlos.pacheco@kemok.io"
        message = "¡Hola, mundo!"
        email = EmailMessage()
        email["From"] = sender
        email["To"] = to
        email["Subject"] = "Correo de prueba"
        email.set_content(message)
        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(sender, "wjlu gasr bmlg ceyf")
        smtp.sendmail(sender, to, email.as_string())
        smtp.quit()
        print('Email enviado a ', to)
    except Exception as error:
        print(error)