from ast import Raise
import re

def verifica_digito_cnpj(cnpj):

    cnpj = re.sub(r'[#*-.,/!]', '', cnpj)
    
    tamanho_cnpj = (len(cnpj))

    if tamanho_cnpj < 14:
        ultimos_quatro_numeros= cnpj[-4:]
        validar_matriz= ultimos_quatro_numeros[0:3]
        if  validar_matriz != '000':
            cnpj = cnpj + '0001'

        cnpj= cnpj[-12:]
        
        calc_num = [6,7,8,9,2,3,4,5,6,7,8,9]

        if len(cnpj) != 12:
            Raise("Por favor insira os 12 digitos do cnpj!")

        cgcPriDig = sum([n*int(v) for n,v in zip(calc_num,cnpj)])%11

        if(cgcPriDig==10):cgcPriDig=0

        cnpj2 = cnpj + str(cgcPriDig)

        cgcSegDig = sum([n*int(v) for n,v in zip([5] + calc_num,cnpj2)])%11
        if(cgcPriDig==10):cgcPriDig=0
        if(cgcSegDig==10):cgcSegDig=0

        cgcDV=cgcPriDig*10+cgcSegDig
        cgcDV=f"{cgcDV:02d}"

        cnpj=cnpj+cgcDV
    else:
        cnpj= cnpj[-14:]
        ultimos_seis_numeros= cnpj[-6:]
        validar_matriz= ultimos_seis_numeros[0:3]
        if  validar_matriz != '000':
            cnpj = ''

    return cnpj