import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import credenciais


para = "rfr3233@gmail.com"

	
def criarjogo(link_jogo):
    servidor_email = smtplib.SMTP_SSL('smtp.titan.email', 465)
    corpo = "<h1>Parabens Por Criar Mais 1 Jogos</h1> <p>Use o link abaixo para entrar em seu jogo e compartilhalo</p><a href='"+link_jogo+"'>"+link_jogo+"</a>"
    servidor_email.login(credenciais.mail, credenciais.senha)
    msg = MIMEMultipart()
    msg['subject'] = "Novo Jogo Criado!!"
    msg.attach(MIMEText(corpo,"html"))
    print(corpo)


    servidor_email.sendmail(credenciais.mail,para, msg.as_string())
    servidor_email.quit()

def recuperar(numero, email):
    servidor_email = smtplib.SMTP_SSL('smtp.titan.email', 465)
    corpo = "<h1>Recebemos seu pedido de recuperação de conta</h1> <p>seu codigo para recuperar a conta é</p><p><strong>"+numero+"</strong></p>"
    servidor_email.login(credenciais.mail, credenciais.senha)
    msg = MIMEMultipart()
    msg['subject'] = "CODIGO DE RECUPERAÇÃO"
    msg.attach(MIMEText(corpo,"html"))
    print(corpo)


    servidor_email.sendmail(credenciais.mail,email, msg.as_string())
    servidor_email.quit()


