import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

def enviar_email(lista_dest, email_bcc, titulo, corpo_email, lista_anexos):
    host = os.environ['host'] # Lê o host no .env
    port = os.environ['port'] # Lê o port no .env
    login = os.environ['login'] # Lê o login no .env
    senha = os.environ['senha'] # Lê a senha no .env

    server = smtplib.SMTP(host, port) # Conecta com o servidor
    server.ehlo() # Verifica o servidor
    server.starttls() # Criptografa a conexão
    server.login(login, senha) # Realiza o login das credenciais no servidor

    email_msg = MIMEMultipart() # Objeto que separa as partes do e-mail
    email_msg['From'] = login # Remetente
    email_msg['To'] = lista_dest # Destinatário
    email_msg['Bcc'] = email_bcc # E-mail oculto
    email_msg['Subject'] = titulo # Título do e-mail
    email_msg.attach(MIMEText(corpo_email, 'plain')) # Corpo do e-mail
    
    if(len(email_bcc)>1): # Caso tenha email oculto, será adicionado ao destinatário
        dest = email_bcc.split(",") + [email_msg['To']]
    else:
        dest = email_msg['To'] # Senão, ficará somente o destinatário
    
    if len(lista_anexos) != 0: # Verifica se existe algum anexo
        for anexo in lista_anexos: # Percorre sobre a lista de anexos
            anexo_quebrado = anexo.split('\\') # Separa o anexo em partes
            attachment = open(anexo, 'rb') # Abre o anexo em modo leitura
            att = MIMEBase('application', 'octet-stream') # Copia o arquivo
            att.set_payload(attachment.read()) # Atribui o tamanho do arquivo
            encoders.encode_base64(att)
            att.add_header('Content-Disposition', f'attachment; filename={anexo_quebrado[-1]}') # Adiciona o nome ao anexo
            attachment.close() # Fecha o anexo
            email_msg.attach(att) # Adiciona o anexo ao e-mail

    server.sendmail(email_msg['From'], dest, email_msg.as_string()) # Envia o e-mail
    server.quit() # Fecha o server

if __name__ == '__main__':
    lista_dest = ['']
    lista_nome = ['']
    email_bcc = ''
    lista_anexos= ['']
    
    for i in range(0, len(lista_dest)):
        titulo='Teste do novo email'
        corpo_email = (f'Boa tarde, {lista_nome[i]}!\nTestando o novo email.\nAtenciosamente, Python.')
        enviar_email(lista_dest[i], email_bcc, titulo, corpo_email, lista_anexos)


    