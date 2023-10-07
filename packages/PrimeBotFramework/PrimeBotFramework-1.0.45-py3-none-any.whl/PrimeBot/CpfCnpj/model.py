from __future__ import annotations
from pydantic import BaseModel

class Endereco(BaseModel):
    logradouro: str
    bairro: str
    cep: str
    cidade: str
    uf: str

class DadosEmpresa(BaseModel):
    razao_social: str
    situacao: str
    endereco: Endereco
    cnpj: str
    delay: float
    saldo: int

class Erro(BaseModel):
    erro: str
    codigo: int