import requests
import json

def autenticacao(username: str, password: str) -> None:
    """ Função para realizar setar os parametros de autenticação

    :param username: nome de usuario
    :param password: senha de autenticação
    :return: token válido por 1h

    """      
    # Iniciando variaveis
    global TOKEN
    url = "https://sso.b2egroup.com.br/api/tokens"
    
    # Instanciando parametros de requisição
    payload = json.dumps({
    "UserName": username,
    "Password": password
    })
    headers = {
    'Content-Type': 'application/json'
    }

    # Realizando requisição
    response = requests.request("POST", url, headers=headers, data=payload)  
    response = response.text

    # inicializando sub strings
    split_after = '","GeneratedAt'
    split_before = '{"AccessToken":"'
 
    # realizando a subtring para o indice do comprimento final
    after_string = response.split(split_after)
    res=after_string[0]
    # realizando a subtring para o indice do comprimento inicial
    before_string = res.split(split_before)
    token_aux=before_string[1]

    # vinculando o valor da string retornada a variavel global
    TOKEN = token_aux
    return TOKEN

def atualizar_parecer_proposta(TOKEN, status, cod_instituicao, proposta, descricao_status, observacoes):
    """ Método para atualização do status da proposta

    :param TOKEN: token de autenticação (str)
    :param status: status da proposta (int)
    :param cod_instituicao: código GUID (str)
    :param proposta: número da proposta a ser atualizada (str)
    :param descricao_status: nome do status por extenso (str)
    :param observacoes: observações livres sobre a proposta (str)

    :return: status code da requisição

    ID do STATUS para atualização:
    :Id 41: "APROVADO - PROCESSO ENCERRADO"
   
    """
    # Inicializando parametros
    base_url = "https://cred-api.b2esistemas.com.br/Parecer/v1.0.0/Pareceres" 
    if not TOKEN:
        raise Exception("Autenticação não definida")
    cod_instituicao= "?codigoInstituicao="+cod_instituicao
    proposta= "&codigoProposta="+proposta

    # Montando o body da requisição
    payload = json.dumps({
    "StatusProposta": {
        "Id": status,
        "Nome": descricao_status,
        "Descricao": descricao_status
    },
    "Observacoes": observacoes
    })
    # Montando o header da requisição
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }

    # Realizando a conexão
    CALL_URL = f"{base_url}{cod_instituicao}{proposta}"
    response = requests.request("PUT", CALL_URL, headers=headers, data=payload)
    
    # Validando o retorno da requisição
    if response.status_code != 200:
            return Exception(response.text)
    
    # return response.status_code

def obter_parecer_proposta(TOKEN, cod_instituicao, proposta):
    """ Método para obtenção do parecer (dados/status) da proposta

    :param TOKEN: token de autenticação (str)
    :param cod_instituicao: código GUID (str)
    :param proposta: número da proposta a ser atualizada (str)
    
    :return: dicionario com os dados da proposta
   
    """
    # Inicializando parametros
    base_url = "https://cred-api.b2esistemas.com.br/Parecer/v1.0.0/Pareceres" 
    if not TOKEN:
        raise Exception("Autenticação não definida")
    cod_instituicao= "?codigoInstituicao="+cod_instituicao
    proposta= "&codigoProposta="+proposta

    # Montando o header da requisição
    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+TOKEN
    }

    # Realizando a conexão
    CALL_URL = f"{base_url}{cod_instituicao}{proposta}"
    response = requests.request("GET", CALL_URL, headers=headers, data=payload)
    
    # Validando o retorno da requisição
    if response.status_code != 200:
            print(response.text)
            return Exception(response.text)
    
    dict_dados_proposta = json.loads(response.text)
    return dict_dados_proposta