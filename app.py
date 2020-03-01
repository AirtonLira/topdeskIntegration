from flask import Flask, jsonify, request
import requests, json
import urllib3

from topdeskintegration.models.categoria import categoria
from topdeskintegration.utils.requestUtils import requestUtils
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
app = Flask(__name__)

@app.route('/gruposoperadores', methods=['GET'])
def gruposoperadores():
    reqUtils = requestUtils(request)

    resultado = requests.get("https://conductor.topdesk.net/tas/api/operatorgroups/lookup", headers=reqUtils.headers, params=reqUtils.parametros,verify=False)
    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    gp = json.dumps(resultado)
    return resultado,str(status_code)

@app.route('/incidentes', methods=['POST'])
def incidentes():
    return

@app.route('/incidentes/anexararquivo', methods=['POST'])
def anexararquivo():
    reqUtils = requestUtils(request)
    urltarget = "https://conductor.topdesk.net/tas/api"
    number = reqUtils.parametros.getlist('number')[0]


    contentsUploadPath = os.listdir("./archives")
    for file in contentsUploadPath:
        filename = "./archives/" + file

        fileName = {'file': open(filename, 'rb')}
        uploadFileUrl = urltarget + '/incidents/number/' + number+ '/attachments'
        uploadFile = requests.post(uploadFileUrl, headers=reqUtils.header,
                                   files=fileName)

    return uploadFile.content,uploadFile.status_code

    return resultado,str(status_code)

@app.route('/categorias', methods=['GET'])
def categorias():
    reqUtils = requestUtils(request)

    resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/categories", headers=reqUtils.header, params=reqUtils.parametros,verify=False)
    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)
    return resultado,str(status_code)

@app.route('/empresas', methods=['GET'])
def empresas():
    reqUtils = requestUtils(request)
    resultado = requests.get("https://conductor.topdesk.net/tas/api/branches", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)
    return resultado, str(status_code)

@app.route('/subcategorias', methods=['GET'])
def subcategorias():
    reqUtils = requestUtils(request)
    resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/subcategories", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)
    return resultado, str(status_code)

@app.route('/tipos', methods=['GET'])
def tipos():
    reqUtils = requestUtils(request)
    resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/call_types", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    return resultado, str(status_code)

if __name__ == '__main__':
    app.run(port=5002,debug=True)