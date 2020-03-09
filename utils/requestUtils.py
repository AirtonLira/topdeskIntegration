import requests, json
from flask import request


class requestUtils:

    def __init__(self, requisicao):
        """Constructor for requestUtils
        
        Arguments:
            requisicao {Request} -- Request object from HTTP operation
        
        Raises:
            Exception: Requisicao nao possui header accept especificado
            Exception: Requisicao nao possui header authrization especificado
        """

        self.requisicao = requisicao

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

    def SetCriarIncidente(self):
    
        """
        Create a JSON for TopDesk API

        Variables used from request:
            descricao {str} -- Description for the incident
            email {str} --
            titulo {str} --
            operator {str} --
            operatorGroup {str} --
        """
        data = {
        "status": "secondLine",
        "request": self.requisicao.form["descricao"] , 
        "caller": { 
            "dynamicName": "[DATASCIENCE]",
            "email": self.requisicao.form["email"], 
            "branch": { 
                "id": "cec824ff-b862-4ed0-88c1-c28a2b5c3ebe",
                "name": "Conductor Tecnologia S/A" 
            }
        },
        "briefDescription": "[DATASCIENCE]" + self.requisicao.form["titulo"] ,
        "category": { "name": "Serviços Emissores"},   
        "subcategory": { "name": "Outros" },
        "callType": { "name": "Evento" },
        "entryType": { "name": "Operador" },
        "impact": { "name": "Urgente" },   
        "urgency": { "name": "Alto" },
        "priority": { 
            "id": "05ababa6-e1af-409c-abd7-23d04dcae5d9",
            "name": "Prioridade - Alta 4hs" 
        },   
        "duration": { "name": "2 horas" },   
        "operator": { "id": self.requisicao.form['operator'] },
        "operatorGroup": { "id": self.requisicao.form['operatorGroup'] },
        "processingStatus": { "id": "a3e2ad64-16e2-4fe3-9c66-9e50ad9c4d69" }
        }
 
        data = json.dumps(data)
        return data
