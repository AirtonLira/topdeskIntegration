from werkzeug.exceptions import HTTPException, NotFound
import logging 
from datetime import datetime
from urllib import request, parse
from constants import *
import json

logging.basicConfig(
        filename="logerror.log",
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        level=logging.INFO
        )

logger = logging.getLogger('API')
time_print = str(datetime.now().strftime("%x %X")) +": "

logger.setLevel(logging.CRITICAL)


class exceptionHandler():
    def __init__(self):
        """
        Construtor of Exception Handler

        Implements atributtes:
        erroCampoInvalido
        erroCampoAusente
        erroTopDesk
        erroNumber
        """
        self.erroCampoInvalido = '[Campo vazio ou não validado]'
        self.erroCampoAusente = '[Campo obrigatório não encontrado]'
        self.erroTopDesk = '[Erro na requisição para o topdesk]'
        self.erroNumber = '[Requisição não possui o number do incidente]'

    def sendException(self,endpoint, text, error, tipo):
        """Send a Exception to Slack Bot and

        Arguments:
            endpoint {str} -- API endpoint
            text {str} -- Error message
            error {Exception} -- Exception object [HTTPException or Exception]
            tipo {str} -- Exception object type in string format
        """
        print(time_print+str(error))
        if tipo == 'HTTPException':
            logging.error(text+str(error))
            self.send_message_to_slack(f"Rota: [{endpoint}] {text} Erro: {str(error.get_response().status)}")
        elif tipo == 'Exception':
            logging.error(text+str(error))
            self.send_message_to_slack(f"Rota: [{endpoint}] {text} Erro: " + str(error).split(')})')[1].replace('\n', ' ') )
        elif tipo == 'NoException':
            logging.error(text+str(error))
            self.send_message_to_slack(f"Rota: [{endpoint}] {text} Erro: {error}")

    def sendExceptionTopDesk(self, endpoint, text, error, url):
         """Send a Exception to Slack Bot from Top Desk

        Arguments:
            endpoint {str} -- API Endpoint
            text {str} -- Error message
            error {Exception} -- Exception object [HTTPException or Exception]
            tipo {str} -- Exception object type in string format
            url {str} -- url from Top Desk
        """
         print(time_print + str(error))
         logging.error(text+str(error))
         self.send_message_to_slack(f"Rota: {endpoint}] {text} {url} ")

    def send_message_to_slack(self, text):
        """Send a message using Slack

        Arguments:
            text {str} -- Error message
        """
        text = text
        post = {"text": "{0}".format(text), "username": "Kelex", "icon_url": "https://w0.pngwave.com/png/128/30/kelex-lar-gand-martian-manhunter-superwoman-firestorm-dc-comics-png-clip-art.png"}

        try:
            json_data = json.dumps(post)
            req = request.Request(URL_SLACK_BOT,
                                data=json_data.encode('ascii'),
                                headers={'Content-Type': 'application/json'})
            resp = request.urlopen(req)
        except Exception as em:
            logging.error(em)


