import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = 'reccirik1@gmail.com'
    from_password = 'Ryn.-001'

    # E-posta başlığı ve içeriği oluşturun
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # E-posta gövdesi
    msg.attach(MIMEText(body, 'plain'))

    # Gmail SMTP sunucusuna bağlanın ve e-postayı gönderin
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderilemedi. Hata: {e}")

# Örnek kullanım
subject = "Test E-posta"
body = "Bu bir test e-postasıdır."
to_email = "recepyeni@gmail.com"

send_email(subject, body, to_email)
