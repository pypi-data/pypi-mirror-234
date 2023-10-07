import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition)


class IntegracaoSendGrid:

    def __init__(self, api_key: str = '', sender: str = ''):
        """ Metodo construtor da classe

        :param api_key: Chave de API do sendGrid
        :param sender: Email que sera usado como remetente

        """
        self.api_key = api_key
        self.sender = sender

    def connection(self):
        """ Função para realizar a conexão com o SENDGRID

        :return: retorna o objeto de conexao 

        """
        try:
            return SendGridAPIClient(self.api_key)
        except Exception as e:
            raise (f"Erro ao criar a conexao com SENDGIRD : {e}")

    def create_message(self, to: list = [''], subject: str = '', html: str = '<p></p>'):
        """ Função para Criar o objeto de email que sera enviado

        :param to: Lista para quem o email sera enviado
        :param subject: String com o assunto do email
        :param Html: String contendo o html que sera adcionado no corpo do email
        :return: retorna o objeto de email

        """
        try:
            return Mail(
                from_email=self.sender,
                to_emails=to,
                subject=subject,
                html_content=html)
        except Exception as e:
            raise (f"Erro ao criar ao criar o corpo do email : {e}")

    def send_email(self, message: object):
        """ Função para Enviar o email

        :param message: Objeto contendo os dados para envio do email

        :return: retorna o status de sucesso ou erro ao enviar o email

        """
        try:
            sd = self.connection()
            response = sd.send(message)
            if response.status_code == 202:
                return "email enviado com sucesso"
            else:
                return f"erro ao enviar o email : {response.text}"
        except Exception as e:
            raise (f"Erro ao enviar email : {e}")

    def send_dynamic_email(self, message: object, template_id: str, dynamic_data: dict):
        """ Função para Enviar o email contendo um template e dados dinamicos

        :param message: Objeto contendo os dados para envio do email
        :param template_id: String contendo o id do template que sera utilizado
        :param dynamic_data: dicionario contendo as chaves e valores para serem subistituidos no corpo da mensagem
        :return: retorna o status de sucesso ou erro ao enviar o email

        """

        try:
            sd = self.connection()
            message.template_id = template_id
            message.dynamic_template_data = dynamic_data
            response = sd.send(message)
            if response.status_code == 202:
                return "email enviado com sucesso"
            else:
                return f"erro ao enviar o email : {response.text}"
        except Exception as e:
            raise (f"Erro ao enviar email dynamic : {e}")

    def add_attachment(self, message: object, path: str, file_mime_type: str, disposition :str,content_id : str):
        """ Função para adcionar anexos ao email

        :param message: Objeto contendo os dados para envio do email
        :param path: String contendo o caminho do arquivo que sera adcionado
        :file_mime_type: String contendo o mime type do arquivos excemplos : pdf = application/pdf , png = image/png
        :disposition: String contendo como o attchment devera ser incluido no email
        :return: retorna o objeto de email com o anexo adcionado

        """
        try:
            data = open(path, "rb").read()
            encoded_file = base64.b64encode(data).decode()
            file_name = os.path.basename(path)

            attachedFile = Attachment(
                FileContent(encoded_file),
                FileName(file_name),
                FileType(file_mime_type),
                Disposition(disposition),
                content_id=content_id,
            )
            message.attachment = attachedFile
            return message
        except Exception as e:
            raise (f"Erro ao adiconar o arquivo nos anexos do email : {e}")
        
    
        