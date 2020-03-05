from flask import Flask, jsonify, request
import requests, json
import urllib3
from datetime import datetime
import os

from models.categoria import categoria
from utilss.requestUtils import requestUtils

from schema import Schema, And, Use, Optional
from werkzeug.exceptions import HTTPException, NotFound

import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL - PATH da conductor https://conductor.topdesk.net/tas/api/

# Parametros obrigatorios criação de incidente
# request - Numero do chamado
# caller - Operador de abertura do chamado
# briefDescription - Breve descrição titulo
# status - Nivel do chamado (ex: secondLine)
# callType - Tipo de chamado (ex: requisição de serviço, dúvida, incidente)
# category - Categoria do chamado (ex: Serviços emissores)
# subcategory - Subcategoria do chamado (ex: Arquivos e relatórios)
# object - null
# location - null
# operatorGroup - Grupo de operadores (ex: INFRA - SCHEDULE)
def send_message_to_slack(text):
    from urllib import request, parse
    import json
    
    post = {"text": "{0}".format(text)}
    
    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
        data=json_data.encode('ascii'),
        headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

app = Flask(__name__)

@app.route('/gruposoperadores', methods=['GET'])
def gruposoperadores():
    reqUtils = requestUtils(request)

    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/operatorgroups/lookup", headers=reqUtils.header, params=reqUtils.parametros,verify=False)
    except Exception as err:
        print("Erro na requição para o topdesk: https://conductor.topdesk.net/tas/api/operatorgroups/lookup")
        print(err)
        raise Exception("Requisição https://conductor.topdesk.net/tas/api/operatorgroups/lookup falhou!")

    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    gp = json.dumps(resultado)
    return resultado,str(status_code)

@app.route('/incidentes', methods=['POST'])
def incidentes():
    return

@app.route('/criarincidente', methods=['POST'])
def criarincidente():
    schema = Schema([{'titulo': And(str, len),
                        'email': And(str, len, lambda s: s.split('@')[1] == 'conductor.com.br'),
                        'descricao': And(str, len)}])
    
    try:
        data = [{'titulo': request.form["titulo"],
                'email': request.form["email"],
                'descricao': request.form["descricao"]}]
        validated = schema.validate(data)
    except HTTPException as e:
        logging.exception("Campo obrigatório não encontrado")
        send_message_to_slack(str(datetime.datetime.now().strftime("%x %X")) +" Dado obrigatorio ausente. Erro: " + str(e.get_response().status))
        return 'Campo obrigatório não encontrado', '400'
    except Exception as error:
        logging.exception("Campo vazio ou não validado")
        send_message_to_slack(str(datetime.datetime.now().strftime("%x %X")) + "Campo vazio ou não validado. Erro: " + str(error).split(')})')[1].replace('\n', ' '))
        return 'Campo vazio ou não validado','400'

    

    reqUtils = requestUtils(request)
    url = "https://conductor.topdesk.net/tas/api/incidents"

    data = {
        "status": "secondLine",
        "request": request.form["descricao"], 
        "caller": { 
            "dynamicName": "[DATASCIENCE]",
            "email": request.form["email"], 
            "branch": { 
                "id": "cec824ff-b862-4ed0-88c1-c28a2b5c3ebe",
                "name": "Conductor Tecnologia S/A" 
            }
        },
        "briefDescription": "[DATASCIENCE]" + request.form["titulo"] ,
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
        "operator": { "id": "060c514e-d1f4-4fed-9c29-33a3e38aa7b1" },
        "operatorGroup": { "id": "060c514e-d1f4-4fed-9c29-33a3e38aa7b1" },
        "processingStatus": { "id": "a3e2ad64-16e2-4fe3-9c66-9e50ad9c4d69" }
    }

    data = json.dumps(data)

    try:
        resultado = requests.post(url, data, headers=reqUtils.header)
        status_code = resultado.status_code
    except Exception as error:
        logging.exception("Erro na requisição para o topdesk: " + url)
        send_message_to_slack(str(datetime.datetime.now().strftime("%x %X")) + " Erro na requisição para o topdesk: " + url + "Erro: " + str(error).split(')})')[1].replace('\n', ' '))
        return 'Erro na requisição para o topdesk','400'
        
    resultado = resultado.content.decode('utf-8')
    send_message_to_slack(str(datetime.datetime.now().strftime("%x %X")) + " Incidente criado com sucesso." )
    
    return resultado,status_code


@app.route('/incidentes/anexararquivo', methods=['POST'])
def anexararquivo():
    reqUtils = requestUtils(request)
    urltarget = "https://conductor.topdesk.net/tas/api"
    number = reqUtils.parametros.getlist('number')[0]

    if number == None:   
        raise Exception("Requisição não possui o number do incidente!") 

    contentsUploadPath = os.listdir("./archives")
    for file in contentsUploadPath:
        filename = "./archives/" + file

        fileName = {'file': open(filename, 'rb')}
        uploadFileUrl = urltarget + '/incidents/number/' + number+ '/attachments'
        
        try:
            uploadFile = requests.post(uploadFileUrl, headers=reqUtils.header,
                                   files=fileName)
        except Exception as error:
            print("Erro na requição para o topdesk: " + uploadFileUrl)
            print(error)            
            raise Exception("Requisição" + uploadFileUrl + "falhou!")

    return uploadFile.content,uploadFile.status_code

    # return resultado,str(status_code)

@app.route('/categorias', methods=['GET'])
def categorias():
    reqUtils = requestUtils(request)

    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/categories", headers=reqUtils.header, params=reqUtils.parametros,verify=False)
    except Exception as error:
        print("Erro na requição para o topdesk: https://conductor.topdesk.net/tas/api/incidents/categories")
        print(error)        
        raise Exception("Requisição https://conductor.topdesk.net/tas/api/incidents/categories falhou!")

    status_code = resultado.status_code
    
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)
    return resultado,str(status_code)

@app.route('/empresas', methods=['GET'])
def empresas():
    reqUtils = requestUtils(request)

    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/branches", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    except Exception as error:
        print("Erro na requição para o topdesk: https://conductor.topdesk.net/tas/api/branches")
        print(error)        
        raise Exception("Requisição https://conductor.topdesk.net/tas/api/branches falhou!")

    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)
    return resultado, str(status_code)

@app.route('/subcategorias', methods=['GET'])
def subcategorias():
    reqUtils = requestUtils(request)

    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/subcategories", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    except Exception as error:
        print("Erro na requição para o topdesk: https://conductor.topdesk.net/tas/api/incidentes/subcategories")
        print(error)        
        raise Exception("Requisição https://conductor.topdesk.net/tas/api/incidents/subcategories falhou!")

    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)
    return resultado, str(status_code)

@app.route('/tipos', methods=['GET'])
def tipos():
    reqUtils = requestUtils(request)
    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/call_types", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    except Exception as error:
        print("Erro na requição para o topdesk: https://conductor.topdesk.net/tas/api/incidentes/call_types")
        print(error)        
        raise Exception("Requisição https://conductor.topdesk.net/tas/api/incidents/call_types falhou!")  

    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    return resultado, str(status_code)


if __name__ == '__main__':
    app.run(port=5002,debug=True)
