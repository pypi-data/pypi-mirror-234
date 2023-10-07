from pathlib import Path
import time
import requests
import json


class DeathByCaptcha:
    URL = "http://api.dbcapi.me/api/captcha"

    def __init__(self, token=None, username=None, password=None):
        self.token = token
        self.username = username
        self.password = password


    def config_h_captcha(self,sitekey,pageurl,proxy="",proxytype=""):
        self.sitekey = sitekey
        self.pageurl = pageurl
        self.proxytype = proxytype
        self.proxy = proxy

    # def config_img_captcha(self,token):
    #     self.token = token

    def resolve_HCaptcha(self,timeout=30):
        hcaptcha_params = {
            "proxy": self.proxy,
            "proxytype": self.proxytype,
            "sitekey": self.sitekey,
            "pageurl": self.pageurl
        }

        payload = {
            'authtoken': self.token,
            'type': '7',
            'hcaptcha_params': json.dumps(hcaptcha_params)
        }

        response = requests.request("POST", self.URL, data=payload)
        if response.status_code != 200:
            return Exception(response.text)
        
        data = {x.split('=')[0]:x.split('=')[1] for x in response.text.split("&")}
        if data["is_correct"] == "0":
            return Exception("Data Sent is not correct!")

        return self.waitSolution(data["captcha"],timeout=timeout) 



    def resolve_ImageCaptcha(self,captchaImage,timeout=30):
        tempo = 0
        while tempo < 30:
            fName = Path(captchaImage).stem + Path(captchaImage).suffix
            payload = {
                'authtoken': self.token,
            }
            files=[
                ('captchafile',(fName,open(captchaImage,'rb'),'application/octet-stream'))
            ]

            response = requests.request("POST", self.URL, data=payload,files=files)
        
            if response.status_code == 200:
                break
            else:
                time.sleep(2)
                tempo=tempo+2
                
        
        if response.status_code != 200:
            return Exception(response.text)

        data = {x.split('=')[0]:x.split('=')[1] for x in response.text.split("&")}
        if data["is_correct"] == "0":
            return Exception("Data Sent is not correct!")
        
        return self.waitSolution(data["captcha"],timeout=timeout)
        
   
    def waitSolution(self,captcha,timeout=30):
        start = time.time()
        response = requests.request("GET", f"{self.URL}/{captcha}")
        data = {x.split('=')[0]:x.split('=')[1] for x in response.text.split("&")}
        if data["is_correct"] == "0":
            return Exception("Data received is not correct!")
        if timeout <= 0:
            return Exception("Timeout solving captcha")
        if data["text"] == "":
            count = time.time()- start
            return self.waitSolution(captcha,timeout-count)
        
        return data["text"]
    
    def resolver_ReCaptcha_V2(self, google_key, page_url, captcha_type=4, proxy='', proxy_type=''):
        """
        Resolve o ReCaptcha V2 usando o serviço DeathByCaptcha.

        Parâmetros:
        google_key (str): A chave pública do site (data-sitekey) do ReCaptcha V2.
        page_url (str): A URL da página onde o ReCaptcha está presente.
        captcha_type (int): O tipo de captcha a ser resolvido (padrão é 4 para ReCaptcha V2).
        proxy (str): (Opcional) Endereço do proxy a ser utilizado (formato IP:porta).
        proxy_type (str): (Opcional) Tipo do proxy.

        Retorna:
        str: O texto do captcha resolvido.
        
        Lança:
        Exception: Caso haja problemas ao resolver o captcha.
        """
        retentativa_request = 0

        token_params = {
            "proxy": proxy,
            "proxytype": proxy_type,
            "googlekey": google_key,
            "pageurl": page_url
        }

        payload = json.dumps(token_params)

        try:
            # Obter CAPTCHA_ID
            if self.token == None:
                response = requests.post(self.URL, data={
                    'username': self.username,
                    'password': self.password,
                    'type': str(captcha_type),
                    'token_params': payload
                })
            else:
                response = requests.post(self.URL, data={
                    'authtoken': self.token,
                    'type': str(captcha_type),
                    'token_params': payload
                })

            if response.status_code != 200:
                raise Exception(response.text)

            data = {x.split('=')[0]: x.split('=')[1] for x in response.text.split("&")}
            if data["is_correct"] == "0":
                raise Exception("Os dados enviados não estão corretos!")

            captcha_id = data['captcha']
            captcha_url = f'http://api.dbcapi.me/api/captcha/{captcha_id}'

            while True:
                captcha_response = requests.get(captcha_url, headers={'Accept': 'application/json'})

                if captcha_response.status_code != 200:
                    raise Exception(f'Falha ao recuperar o captcha. Código de status: {captcha_response.status_code}')

                if captcha_response.json()['text'] == '':
                    retentativa_request += 1
                    time.sleep(2)
                else:
                    break

                if retentativa_request == 60:
                    raise Exception(f"Falha ao recuperar o captcha após {retentativa_request} tentativas.")

            captcha_data = captcha_response.json()
            return captcha_data['text']
        
        except Exception as e:
            raise Exception(f'Erro ao resolver o captcha: {e}')