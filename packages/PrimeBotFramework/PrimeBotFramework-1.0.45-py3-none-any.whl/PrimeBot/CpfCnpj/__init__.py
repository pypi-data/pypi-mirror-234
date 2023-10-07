import requests
from PrimeBot.CpfCnpj.model import Endereco, DadosEmpresa
from PrimeBot.CpfCnpj.api_codes import Package, Error

def set_token(token: str) -> None:
    global TOKEN
    TOKEN = token


def consulta_cnpj_pacote_C(cnpj: str) -> dict:
    base_url = "https://api.cpfcnpj.com.br/"
    if not TOKEN:
        raise Exception("Token não definido")
    CALL_URL = f"{base_url}/{TOKEN}/{Package.CNPJ_C.value}/{cnpj}"
    response = requests.get(CALL_URL)
    response_json = response.json()
    error_list = [
        Error.CNPJ_INCOMPLETO.value,
        Error.CNPJ_INVALIDO.value,
        Error.CNPJ_INEXISTENTE.value,
        Error.TOKEN_INVALIDO.value,
        Error.FORNECEDOR_INDISPONIVEL.value,
        Error.IMPOSSIVEL_CONSULTAR.value,
        Error.CONTA_BLOQUEADA.value,
        Error.CREDITOS_INSUFICIENTES.value,
        Error.PACOTE_INVALIDO.value,
    ]

    if response_json["status"]:
        endereco = response_json["matrizEndereco"]
        resultado = DadosEmpresa(
            razao_social=response_json["razao"],
            cnpj=response_json["cnpj"],
            situacao=response_json["situacao"]["nome"],
            endereco= Endereco(
                logradouro=endereco["logradouro"],
                bairro=endereco["bairro"],
                cep=endereco["cep"],
                cidade=endereco["cidade"],
                uf=endereco["uf"],
            ),
            delay=response_json["delay"],
            saldo=response_json["saldo"]
        )
    elif response_json["erroCodigo"] == Error.BLACKLIST.value:
        erro=response_json["blacklist"]["motivo"]
        codigo=response_json["erroCodigo"]
        raise Exception(str(codigo) + ": " + erro)
    elif response_json["erroCodigo"] in error_list:
        erro=response_json["erro"]
        codigo=response_json["erroCodigo"]
        raise Exception(str(codigo) + ": " + erro)
    else:
        raise Exception("999: Erro desconhecido")

    return resultado.dict()