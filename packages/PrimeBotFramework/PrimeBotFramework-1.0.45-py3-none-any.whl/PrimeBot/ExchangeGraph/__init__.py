from ast import Raise
import base64
from dataclasses import Field, dataclass, field
from email.policy import default
from functools import wraps
import msal
import requests
import json
from dateUts import *
import os


@dataclass
class OauthParams:
    username     : str
    password     : str
    client_id    : str
    client_secret: str
    tenant_id    : str
    user_id      : str
    base_url     : str = field(default='')
    authority    : str = field(default='')

class ExchangeAuth:
    last_token_key_at = None
    token_code        = None
    exp_secs          = None

    def __init__(self, config: OauthParams):
    
        self.config = config
        self.config.authority = f"https://login.microsoftonline.com/{self.config.tenant_id}"
        self.config.base_url = f"https://graph.microsoft.com/v1.0/users/{self.config.user_id}"
        self.app = msal.ConfidentialClientApplication(
            client_id=config.client_id,
            client_credential=config.client_secret,
            authority=config.authority)

    def update_token(self):
        # TODO Avaliar se pode vir como parametro
        scopes = ["https://graph.microsoft.com/.default"]
        result = None
        result = self.app.acquire_token_by_username_password(
            username=self.config.username,
            password=self.config.password,
            scopes=scopes
        )
        if not result:
            print(
                "Não existe um token em cache. Criando um novo do Azure Active Directory.")
        result = self.app.acquire_token_for_client(scopes=scopes)
        if "access_token" in result:
            print(result)
            #print("Access token - " + result["access_token"])
            self.token_code = result["access_token"]
            self.last_token_key_at = today()
            self.exp_secs = result["expires_in"]
            return (True, '')
        else:
            return (False, result)

    def validate_token(self):
        expired = False
        if self.last_token_key_at:
            expired = today() >= dateAdd(self.last_token_key_at, self.exp_secs-10*60, 'seconds')

        if not self.last_token_key_at or expired:
            resp = self.update_token()
            if not resp[0]:
                raise Exception(f"Error generating new Token:{resp[1]}")
            else:
                print("New token generated!")

    @property
    def headers(self):
        self.validate_token()
        return {"Authorization": f"Bearer {self.token_code}"}

    @property
    def token(self):
        self.validate_token()
        self.token_code

class OFolder:
    def __init__(self,jsonObj:dict,cnt:ExchangeAuth):
        self.__dict__ = jsonObj
        self.exgAuth = cnt

    def childFolders(self):
        
        endpoint = f"{self.exgAuth.config.base_url}/mailFolders/{self.id}/childFolders"
        r = requests.get(url=endpoint, headers=self.exgAuth.headers)
        if r.status_code != 200: raise Exception("Error:" + r.text)
        fdrs = [OFolder(x,self.exgAuth) for x in r.json()["value"]]
        return fdrs

    def get_mails(self,**kargs):
        params = "&".join([f"{k}={v}" for k,v in kargs.items() if v is not None])
        endpoint = f"{self.exgAuth.config.base_url}/mailFolders/{self.id}/messages?{params}"
        emailList = []
        data = None

        while True:
            url = endpoint if not data else data["@odata.nextLink"]
            r = requests.get(url, headers=self.exgAuth.headers)
            if r.status_code != 200:
                raise Exception("Error:" + r.text)
            data = r.json()
            emailList += data["value"]
            if not "@odata.nextLink" in data: break

        return [OMail(x,self.exgAuth) for x in emailList]

    def __repr__(self):
        return f"<OFolder {self.displayName}>"

class OMail:
    exgAuth = None

    def __init__(self,jsonObj:dict,cnt:ExchangeAuth):
        self.create(jsonObj)
        self.exgAuth = cnt

    def create(self,jsonObj):
        jsonObj["_from"] = jsonObj["from"]
        exgAuth = self.exgAuth
        self.__dict__ = jsonObj
        self.exgAuth = exgAuth

    def set_read(self,isRead:bool):
        endpoint = f"{self.exgAuth.config.base_url}/messages/{self.id}"
        body = {"isRead": isRead}
        r = requests.patch(url=endpoint, headers=self.exgAuth.headers, json=body)
        if r.status_code != 200:
            raise Exception("Error:" + r.text)
        self.create(r.json())
        


    def __repr__(self):
        return f"<Omail {self._from['emailAddress']['name']}>"

class OMessage:
    subject = None
    body = None
    def __init__(self,cnt:ExchangeAuth):
        self.exgAuth = cnt
    
    def set_subject(self,subject):
        self.subject = subject
    
    def set_body(self,contentType,content):
        self.body = {
            "contentType": contentType,
            "content"    : content
        }
    
    def set_toRecipients(self,address:list):
        self.toRecipients = [
            {"emailAddress":{"address":x}} for x in address
        ]
    
    def set_attachments(self,attachments:list):
        atts = []
        for att in attachments:
            fl_binary = open(att,"rb").read()
            encoded_file = base64.b64encode(fl_binary)
            data = {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": os.path.basename(att),
                    #"contentType": "reference",
                    "contentBytes": encoded_file.decode("utf-8")
                }
            atts.append(data)
        self.attachments = atts
    
    def send(self):
        payload = {
            "message":{
                "subject"     : self.subject,
                "body"        : self.body,
                "toRecipients": self.toRecipients,
                "attachments" : self.attachments
            }

        }
        endpoint = f"{self.exgAuth.config.base_url}/sendMail"
        r = requests.post(url=endpoint, headers=self.exgAuth.headers, json=payload)
        if r.status_code not in [200,202]:
            raise Exception("Error:" + r.text)
            
        return True

class ExchangeGraph:

    def __init__(self,username,password,client_id,client_secret,tenant_id,user_id):
        config = OauthParams(
            username      = username,     
            password      = password,     
            client_id     = client_id,    
            client_secret = client_secret,
            tenant_id     = tenant_id,    
            user_id       = user_id    
        )
        
        self.exgAuth = ExchangeAuth(config=config)
    
    def get_folders(self):
        endpoint = f"{self.exgAuth.config.base_url}/mailFolders"
        r = requests.get(url=endpoint, headers=self.exgAuth.headers)
        if r.status_code != 200:
            raise Exception("Error:" + r.text)

        return [OFolder(x,self.exgAuth) for x in r.json()["value"]]
    
    def get_folder_by_path(self,path,current_folder=None):
        dirs = os.path.normpath(path).split(os.sep)
        if not dirs: raise Exception("Please insert a valid path")

        fdr = None
        if not current_folder:
            main_folders = self.get_folders()
            fdr = [x for x in main_folders if x.displayName == dirs[0]]
        else:
            chlds = current_folder.childFolders()
            fdr = [x for x in chlds if x.displayName == dirs[0]]
        
        if len(dirs) == 1: return fdr[0]
        return self.get_folder_by_path("/".join(dirs[1:]),fdr[0])

    def newMessage(self):
        return OMessage(self.exgAuth)
        

# import glob

# if __name__ == "__main__":

#     username      = "rpa.cotacaoautomatica@primecontrol.com.br",
#     password      = "Cpfl@2022*",
#     client_id     = "ef15e8b4-6087-491c-a939-97e985f36ddf",
#     client_secret = "~m08Q~y5QAd6M3fD~SZRoalE2WCrAplofO9Kncox",
#     tenant_id     = "3c924ffe-f013-49fb-ab9c-abc7152969ad",
#     user_id       = "8d9a5d16-12ca-40a7-96f0-82266fde95d0"

#     exchange_client = ExchangeGraph(username=username,password=password,client_id=client_id,client_secret=client_secret,tenant_id=tenant_id,user_id=user_id)

#     #ENVIANDO EMAIL
#     msg = exchange_client.newMessage()
#     msg.set_subject("test Subject")
#     msg.set_body("Text","Esse e um email de teste!")
#     msg.set_toRecipients(["melque_ex@yahoo.com.br"])
#     msg.set_attachments(glob.glob(r"C:\Users\melque\Documents\test\*.*"))
#     msg.send()
 
#     #RETORNANDO PASTAS
#     folders = exchange_client.get_folders()

#     #RETORNANDO PASTA ESPECIFICA
#     subf = exchange_client.get_folder_by_path("Teste/subfolder1")

#     #LENDO EMAILS DE UMA PASTA
#     mails = subf.get_mails()

#     #LENDO EMAILS NAO LIDOS
#     mails = subf.get_mails(filter="isRead eq true") #PODE ADCIONAR O PARAMETRO -> top=1 PRA TRAZER SO 1 ITEM

#     # MARCANDO O EMAIL COMO LIDO
#     mails[0].set_read(False)

#     # MARCANDO O EMAIL COMO NAO LIDO
#     mails[0].set_read(True)


