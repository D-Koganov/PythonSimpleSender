from email.policy import default
import smtplib
import sys
import os
import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

client_data_file = 'client_data.txt'
client_mail_text_file = 'mail_text.txt'
client_mail_subject_file = 'mail_subject.txt'
client_mail_data_folder = 'attachments'
receiver_separator = ','
#codecs = ["cp1252", "utf-16", "utf-8", "cp437", "utf-16be"]
default_encoding = "utf-8"

class ClientData():
    def __init__(self, server, port, name, pwd, receiver):
        self.server = server
        self.port = port
        self.name = name
        self.pwd = pwd
        self.receiver = receiver

    def isOk(self):
        return self.server and self.port and self.name and self.pwd and self.receiver

def get_client_data() ->ClientData:
    with open(client_data_file, 'r') as client_data:
        server = client_data.readline().split(':')[1].strip()
        port = int(client_data.readline().split(':')[1].strip())
        name = client_data.readline().split(':')[1].strip()
        pwd = client_data.readline().split(':')[1].strip()
        receiver = client_data.readline().split(':')[1].strip()
        if (receiver_separator in receiver):
            receiver = [x.strip() for x in receiver.split(receiver_separator)]
        return ClientData(server, port, name, pwd, receiver)

def get_subject(codec = default_encoding) ->str:
    with open(client_mail_subject_file, 'r', encoding=codec) as client_subject:
        return client_subject.readline()

def get_text(codec = default_encoding) -> list:
    with open(client_mail_text_file, 'r', encoding=codec) as client_text:
        lines_list = client_text.readlines()
    return lines_list

def send_email(client_data :ClientData, subject :str, text :list, attachments :list):
    msg_text = MIMEText('\n'.join(text))
    if (attachments):
        msg = MIMEMultipart()
        msg.attach(msg_text)
        for file_path in attachments:
            filename = os.path.basename(file_path)
            ftype, encoding = mimetypes.guess_type(file_path)
            file_type, subtype = ftype.split('/')
            if (file_type == 'text'):
                with open(file_path) as f:
                    msg_part = MIMEText(f.read())
            elif (file_type == 'image'):
                with open(file_path, 'rb') as f:
                    msg_part = MIMEImage(f.read(), subtype)
            elif (file_type == 'audio'):
                with open(file_path, 'rb') as f:
                    msg_part = MIMEAudio(f.read(), subtype)
            elif (file_type == 'application'):
                with open(file_path, 'rb') as f:
                    msg_part = MIMEApplication(f.read(), subtype)
            else:
                with open(file_path, 'rb') as f:
                    msg_part = MIMEBase(file_type, subtype)
                    msg_part.set_payload(f.read())
                    encoders.encode_base64(msg_part)
            msg_part.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(msg_part)
    else:
        msg = msg_text
    if (subject):
        msg["Subject"] = subject
    server = smtplib.SMTP(client_data.server, client_data.port, timeout=10)
    server.starttls()
    server.login(client_data.name, client_data.pwd)
    server.sendmail(client_data.name, client_data.receiver, msg.as_string())


def main():
    if len(sys.argv) > 1:
        print("Using custom encoding!!!")
        text_codec = sys.argv[1]
        print(text_codec)
    else:
        text_codec = default_encoding
        print("Using default encoding: "+text_codec)
    print('Getting client data....')
    client_data = get_client_data()
    if not client_data.isOk():
        print("Error in client data. Exiting")
        return
    print("Sending to:")
    print(client_data.receiver)
    print()
    print()
    print('Getting subject ....')
    subject = get_subject(text_codec)
    print('Getting text....')
    text = get_text(text_codec)
    print('Getting attachment paths....')
    if os.path.exists(client_mail_data_folder):
        attachment = [os.path.join(client_mail_data_folder, x) for x in os.listdir(client_mail_data_folder)]
    else: 
        attachment = []
    print('Trying to send email....')
    send_email(client_data, subject, text, attachment)
    print('Message sent')

if __name__ == "__main__":
    main()
    print('Done')
