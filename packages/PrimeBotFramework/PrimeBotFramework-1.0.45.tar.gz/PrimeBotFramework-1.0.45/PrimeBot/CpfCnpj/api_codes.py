from enum import Enum

class Package(Enum):
    """
    `Enum` with the package id's for the CPF and CNPJ API's.
    source: https://www.cpfcnpj.com.br/dev/#pacotes
    """
    CPF_A = 1
    CPF_B = 7
    CPF_C = 2
    CPF_D = 8
    CPF_E = 9
    CPF_F = 3
    CPF_G = 13
    CPF_H = 14
    CNPJ_A = 4
    CNPJ_B = 5
    CNPJ_C = 10
    CNPJ_D = 6
    CNPJ_G = 12

class Error(Enum):
    CNPJ_INVALIDO = 200
    CNPJ_INCOMPLETO = 201
    CNPJ_INEXISTENTE = 202
    TOKEN_INVALIDO = 1000
    CREDITOS_INSUFICIENTES = 1001
    CONTA_BLOQUEADA = 1002
    BLACKLIST = 1003
    PACOTE_INVALIDO = 1004
    IMPOSSIVEL_CONSULTAR = 1005
    FORNECEDOR_INDISPONIVEL = 1006