import mimetypes
import os
import smtplib

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def adiciona_anexo(msg, filename):
    print(filename)
    if not os.path.isfile(filename):
        return

    ctype, encoding = mimetypes.guess_type(filename)

    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'

    maintype, subtype = ctype.split('/', 1)

    if maintype == 'text':
        with open(filename) as f:
            mime = MIMEText(f.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(filename, 'rb') as f:
            mime = MIMEImage(f.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(filename, 'rb') as f:
            mime = MIMEAudio(f.read(), _subtype=subtype)
    else:
        with open(filename, 'rb') as f:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(f.read())

        encoders.encode_base64(mime)

    mime.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(mime)

de = 'chamados@palmed.com.br'
para = ['joeltonsmoura1@gmail.com']

msg = MIMEMultipart()
msg['From'] = de
msg['To'] = ', '.join(para)
msg['Subject'] = 'Backup pfSense admin'

# Corpo da mensagem

# Arquivos anexos.
adiciona_anexo(msg, './config.XML')

raw = msg.as_string()

smtp = smtplib.SMTP('smtp.palmed.com.br', 25)
smtp.login('chamados@palmed.com.br', 'Eu123456@')
print('Passou aqui')
smtp.sendmail(de, para, raw)
smtp.quit()

