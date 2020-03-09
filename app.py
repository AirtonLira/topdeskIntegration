from libs import *

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

# Posting to a Slack channel
exc = exceptionHandler()
logger = logging.getLogger('API')

app = Flask(__name__)

@app.route('/gruposoperadores', methods=['GET'])
def gruposoperadores():
    reqUtils = requestUtils(request)

    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/operatorgroups/lookup", headers=reqUtils.header, params=reqUtils.parametros,verify=False)
    except Exception as err:
        exc.sendException("/gruposoperadores", exc.erroTopDesk, err, 'https://conductor.topdesk.net/tas/api/operatorgroups/lookup')
        return exc.erroTopDesk, '400'

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
                        'descricao': And(str, len),
                        'operator': And(str, len),
                        'operatorGroup': And(str, len)}])
    try:
        data = [{'titulo':request.form["titulo"],
                'email':request.form["email"],
                'descricao':request.form["descricao"],
                'operator': request.form["operator"],
                'operatorGroup': request.form["operatorGroup"]}]
    except HTTPException as e:
        exc.sendException("/criarincidente", exc.erroCampoAusente, e, 'HTTPException')
        return exc.erroCampoAusente,'400'
    try:
        schema.validate(data)
    except Exception as error:
        exc.sendException("/criarincidente", exc.erroCampoInvalido, error, 'Exception')
        return exc.erroCampoInvalido,'400'

    reqUtils = requestUtils(request)
    url = "https://conductor.topdesk.net/tas/api/incidents"

    data = reqUtils.SetCriarIncidente()

    try:
        resultado = requests.post(url, data, headers=reqUtils.header)
        id_incidente = requests.get('https://conductor.topdesk.net/tas/api/incidents?page_size=1&order_by=creation_date+DESC&fields=number',headers=reqUtils.header, params=reqUtils.parametros,verify=False)
        status_code = resultado.status_code

    except Exception as error:
        exc.sendExceptionTopDesk("/criarincidente", exc.erroTopDesk, error, url)
        return exc.erroTopDesk,'400'

    resultado = resultado.content.decode('utf-8')
    id_incidente = id_incidente.content.decode('utf-8')
    match = re.search('\w\d+\W\d+', id_incidente).group()

    # Resolver exceção
    exc.send_message_to_slack(str(datetime.now().strftime("%x %X")) + " Incidente de ID: "  + match + " criado com sucesso.")
    logger.info(str(datetime.now().strftime("%x %X")) + " Incidente de ID: "  + match + " criado com sucesso.")

    return resultado, status_code

# Exception não implementada, endpoint não funciona
@app.route('/incidentes/anexararquivo', methods=['POST'])
def anexararquivo():
    reqUtils = requestUtils(request)
    urltarget = "https://conductor.topdesk.net/tas/api"

    if len(reqUtils.parametros.getlist('number')) == 0:
        exc.sendException('/incidentes/anexararquivo', exc.erroCampoAusente, "Parâmetro com o Number do incidente deve ser passado na URL", 'NoException')
        return exc.erroCampoAusente,'400'

    number = reqUtils.parametros.getlist('number')[0]

    f = request.files["file"]
    f.save("./archives/"+ f.filename)
    f.close()

    contentsUploadPath = os.listdir("./archives")
    for file in contentsUploadPath:
        filename = "./archives/" + file

        fileName = {'file': open(filename, 'rb')}
        uploadFileUrl = urltarget + '/incidents/number/' + number+ '/attachments'
        
        try:
            uploadFile = requests.post(uploadFileUrl, headers=reqUtils.header,
                                   files=fileName)
        except Exception as error:
            exc.sendExceptionTopDesk('/incidentes/anexararquivo', exc.erroTopDesk, error, urltarget)
            os.remove("./archives/"+ f.filename)            
            return exc.erroTopDesk, "400"
            #print("Erro na requição para o topdesk: " + uploadFileUrl)
            #print(error) 
            #raise Exception("Requisição" + uploadFileUrl + "falhou!")
    
    os.remove("./archives/"+ f.filename) 

    #Verificar retorno
    return uploadFile.content, uploadFile.status_code

@app.route('/categorias', methods=['GET'])
def categorias():
    reqUtils = requestUtils(request)
    url = "https://conductor.topdesk.net/tas/api/incidents/categories"
    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/categories", headers=reqUtils.header, params=reqUtils.parametros,verify=False)
    except Exception as error:
        exc.sendExceptionTopDesk('/categorias', exc.erroTopDesk, error, url)
        return exc.erroTopDesk, "400"

    status_code = resultado.status_code
    
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)

    return resultado,str(status_code)

@app.route('/empresas', methods=['GET'])
def empresas():
    reqUtils = requestUtils(request)
    url = "https://conductor.topdesk.net/tas/api/branches"

    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/branches", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    except Exception as error:
        exc.sendExceptionTopDesk('/empresas', exc.erroTopDesk, error, url)
        return exc.erroTopDesk, "400"
        
    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)

    return resultado, str(status_code)

@app.route('/subcategorias', methods=['GET'])
def subcategorias():
    reqUtils = requestUtils(request)
    url = "https://conductor.topdesk.net/tas/api/incidents/subcategories"

    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/subcategories", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    except Exception as error:
        exc.sendExceptionTopDesk('/subcategorias', exc.erroTopDesk, error, url)
        return exc.erroTopDesk, "400"
    
    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')
    cg = json.loads(resultado)
    return resultado, str(status_code)

@app.route('/tipos', methods=['GET'])
def tipos():
    reqUtils = requestUtils(request)
    url = "https://conductor.topdesk.net/tas/api/incidents/call_types"

    try:
        resultado = requests.get("https://conductor.topdesk.net/tas/api/incidents/call_types", headers=reqUtils.header,params=reqUtils.parametros, verify=False)
    except Exception as error:
        exc.sendExceptionTopDesk('/tipos', exc.erroTopDesk, error, url)
        return exc.erroTopDesk, "400"

    status_code = resultado.status_code
    resultado = resultado.content.decode('utf-8')

    return resultado, status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)
