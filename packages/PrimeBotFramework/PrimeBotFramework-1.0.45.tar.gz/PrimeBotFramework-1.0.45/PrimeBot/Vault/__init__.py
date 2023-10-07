from requests.exceptions import ConnectionError
from hvac.exceptions import InvalidPath
from dataclasses import dataclass
import traceback
import hvac
import os

""" 
    ============== DESCRICAO GERAL ============
        Classe para conectar o Vault e obter os dados
        para execução do robô

    ================= CLIENT =================
        Obtem o cliente conectado no Vault

        OUTPUT:
            type:<TODO>
            Obs:Retorna os vault object

    ============= GET_CREDENTIALS ============
        Obtem as credenciais do Vault

        INPUT:
            - secrets_path: str =  Especifica os dados do vault que serão utilizados
        OUTPUT:
            type:<Dict>
            Obs:Retorna os dados da secrets
        RAISES:
            - Exception : Path ou chave inválida        
"""

@dataclass
class Messages:
    conError :str = """
                        Verifique se o Vault está em execução e se as variáveis de
                        ambiente, descritas na documentação dessa
                        Lib, estão configuradas
                    """
    authError :str = "Verifique o token configurado na variável de ambiente"


class Vault:
    
    def __init__(self,token):
        self.client = self.__client(token)

    def __client(self,token):
        try:
            client = hvac.Client(token=token)
            
            if not client.is_authenticated():
                raise Exception(Messages.authError)

            return client
        except ConnectionError:
            raise Exception(f'{traceback.format_exc()} \n\n{Messages.conError}')

    def get_credentials(self,path, mount_point=None):
        secret = os.path.basename(os.path.normpath(path))
        val = self.verify_secret(mount_point=mount_point,secret=secret)
        if not val:
            raise Exception("Secret '{secret}' not found!")

        try:
            hvreponse = self.client.secrets.kv.v2.read_secret_version(mount_point=mount_point,path=path)
            return hvreponse['data']['data']
        except InvalidPath:
            raise Exception(f'{traceback.format_exc()}')
        except KeyError:
            raise Exception(f'{traceback.format_exc()}')
    def verify_secret(self,mount_point,secret,path=""):
        try:
            hvreponse = self.client.secrets.kv.v2.list_secrets(mount_point=mount_point,path=path)
            keys = hvreponse['data']["keys"]
            return secret in keys
        except InvalidPath:
            raise Exception(f'{traceback.format_exc()}')
        except KeyError:
            raise Exception(f'{traceback.format_exc()}')


# token = "s.WrhdYlmstBXsdNIL2ztsccPF"
# a = VaultClient(token)
# cred = a.get_credentials("juju","kv")
# a=1



