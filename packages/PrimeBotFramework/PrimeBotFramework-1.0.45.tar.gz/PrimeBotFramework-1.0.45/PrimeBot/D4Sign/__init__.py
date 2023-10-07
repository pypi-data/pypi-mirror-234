import requests
import json


def set_token(token: str, key: str) -> None:
    """ Função para realizar setar os parametros de autenticação

    :param token: token de autenticação
    :param key: cryptkey de autenticação
    
    """      
    global TOKEN, CRYPTKEY
    TOKEN = token
    CRYPTKEY = key

def consultar_documentos_por_fase(fase: str):
    """ Função para consultar todos os documentos que estiverem na fase informada

    :param fase: número da fase
    :type fase: str
    :return: lista de documentos

    ID da FASE que deverá ser listado:
    :ID 1 - Processando
    :ID 2 - Aguardando Signatários
    :ID 3 - Aguardando Assinaturas
    :ID 4 - Finalizado
    :ID 5 - Arquivado
    :ID 6 - Cancelado
    :ID 7 - Editando
    
    """
    
    base_url = "https://secure.d4sign.com.br/api/v1/documents/"
    if not TOKEN or not CRYPTKEY:
        raise Exception("Autenticação não definida")
    tokenAPI= "status?tokenAPI="+TOKEN
    cryptKey= "&cryptKey="+CRYPTKEY

    # Realizando a primeiro conexão
    CALL_URL = f"{base_url}/{fase}/{tokenAPI}{cryptKey}"
    # "https://secure.d4sign.com.br/api/v1/documents/"+fase+"/status?tokenAPI="+TOKEN+"&cryptKey="+CRYPTKEY
    headers = {"accept": "application/json"}
    response = requests.get(CALL_URL, headers=headers)

    # Capturando o total de paginas retornadas
    response_dict = json.loads(response.text)
    total_pages = response_dict[0]["total_pages"]
    print(total_pages)

    # Iniciando lista de documentos
    lista_documentos = []

    # Realizando loop nas paginas retornadas
    for page in range(total_pages):
        page=page+1
        page = "&pg="+str(page)
        
        # Montando a URL de chamada
        CALL_URL = f"{CALL_URL}{page}"
        response = requests.get(CALL_URL, headers=headers)
        
        # Realizando loop nos documentos da pagina
        documentos = json.loads(response.text)
        for documento in documentos:
            # print(documento)
            try:
                # Capturando parametros do documento
                id = documento["uuidDoc"]
                num_proposta = documento["nameDoc"]
                # Inserindo os paramentos na lista
                documento_retornado =(id, num_proposta)      
                lista_documentos.append(documento_retornado)
            except:
                pass


    # # Criando o dicionario de proposta e inserindo a lista como parametro
    # dict_propostas = {
    # 'documento': lista_documentos_assinados
    # }
            
    # Retorna lista com documentos
    return  lista_documentos
