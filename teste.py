import json

from flask import Flask, jsonify
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL - PATH da conductor https://conductor.topdesk.net/tas/api/

# Parametros obrigatorios criação de incidente
# request - Numero do chamado
# briefDescription - Breve descrição titulo
# status - Nivel do chamado (ex: secondLine)
# callType - Tipo de chamado (ex: requisição de serviço, dúvida, incidente)
# category - Categoria do chamado (ex: Serviços emissores)
# subcategory - Subcategoria do chamado (ex: Arquivos e relatórios)
# object - null
# location - null
# operatorGroup - Grupo de operadores (ex: INFRA - SCHEDULE)

headers = {'Authorization': "",
           'content-type': "multipart/form-data"}
files = {'file': ('teste2.jpg',open('teste2.jpg', 'rb'))}


with open('teste2.jpg', 'rb') as f:
    r = requests.post('http://conductor.topdesk.net/tas/api/incidents/number/I2002-3026/attachments', files={'teste2.jpg': f},headers=headers,verify=False)

# resultado = requests.post("http://conductor.topdesk.net/tas/api/incidents/number/I2002-3026/attachments",headers=headers,data=files,verify=False)
status_code = r.status_code
# resultado = resultado.content.decode('utf-8')
# resultado_json = json.dumps(resultado)
print(str(status_code))




