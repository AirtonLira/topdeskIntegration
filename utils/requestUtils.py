import requests
from flask import request


class requestUtils:

    def __init__(self, requisicao):
        if requisicao.headers['Accept'] == None or requisicao.headers['Accept'] == "":
            raise Exception("Requisição não possui header accept especificado!")
        else:
            self.Content_type = requisicao.headers['Accept']

        if requisicao.headers['Authorization'] == None or requisicao.headers['Authorization'] == "":
            raise Exception("Requisição não possui header authorization especificado!")
        else:
            self.Authorization = requisicao.headers['Authorization']

        self.header = {'Authorization': self.Authorization,'Accept': 'application/json'}
        self.parametros = requisicao.args
        self.token = ""

