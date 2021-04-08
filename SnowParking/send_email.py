import smtplib
from email.mime.text import MIMEText

class Email:

    def __init__(self):
        
        self.mail_host = 'smtp.gmail.com'
        self.mail_port = 465
        self.mail_user = 'xmlyqing00@gmail.com'  
        self.mail_pwd = 'xmlyqing2014'   
        # self.receivers = ['account@lyq.me', 'Ruiqi.li@Colorado.edu', 'wenhanou1994@gmail.com']  
        self.receivers = ['account@lyq.me']
        
    def send(self, subject, content):
        
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = subject 
        message['From'] = self.mail_user

        try:
            server_ssl = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
            server_ssl.ehlo()
            server_ssl.login(self.mail_user, self.mail_pwd)
            print('Login succeeded.')
            
            for receiver in self.receivers:
                message['To'] = receiver
                server_ssl.sendmail(self.mail_user, receiver, message.as_string())
                print(f'Send email to {receiver} succeeded.')
            server_ssl.close()
            

        except smtplib.SMTPException as e:
            print('Send email error', e)
