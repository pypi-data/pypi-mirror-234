import os
import logging

class Cnab750():
    """
        Métodos de leitura de dados do CNAB 750 - Pagamentos Instantâneos
    """

    def retornar_arquivos_diretorio(self, caminho_diretorio: str) -> list:
        """Retorna os arquivos de um diretorio

        Args:
            caminho_diretorio (str): caminho do diretorio

        Returns:
            list: caminho dos arquivos encontrados
        """
        arquivos = []
        for filename in os.listdir(caminho_diretorio):
            file_path = os.path.join(caminho_diretorio, filename)
            if os.path.isfile(file_path):
                arquivos.append(file_path)
        return arquivos

    def ler_arquivo(self, caminho_arquivo: str) -> list:
        """Efetua a leitura do arquivo de retorno

        Args:
            caminho_arquivo (str): path do arquivo de retorno

        Returns:
            list: linhas do arquivo
        """
        with open(caminho_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
        return linhas

    def identificar_versao_arquivo(self, linhas: list) -> str:
        """Identificar qual a versão do arquivo

        Args:
            linhas (list): conteudo do arquivo

        Returns:
            str: versão do arquivo cnab 750
        """
        return self.extrair_campo(linhas[0], 741, 744)

    def identificar_codigo_registro(self, linha: str) -> str:
        """Identificar qual o tipo de registro

        Args:
            linha (str): linha do arquivo lido

        Returns:
            str: codigo de registro
        """
        codigo_registro = self.extrair_campo(linha, 0, 0)
        if codigo_registro == '0':
            return 'HEADER'
        elif codigo_registro == '1':
            return 'DETALHE'
        if codigo_registro == '4':
            return 'EMV'
        if codigo_registro == '9':
            return 'TRAILER'
        else:
            return ''
        
    def extrair_campo(self, linha: str, index_ini: int, index_fim: int) -> str:
        """Extrai um valor de um campo

        Args:
            linha (str): linha com as informações
            index_ini (int): indice do início
            index_fim (int): indice do fim

        Returns:
            str: dado
        """
        if index_ini == index_fim:
            return linha[index_ini].strip()
        else:
            return linha[index_ini:index_fim].strip()
    
    def extrair(self, tipo_arquivo: str, linhas: list) -> list:
        """Extrai os dados do arquivo

        Args:
            tipo_arquivo (str): tipo 'remessa' ou tipo 'retorno'
            linhas (list): linhas do arquivo

        Returns:
            list[dict]: lista de dicionarios contendo a informação de cada linha
        """
        dados = []
        for linha in linhas:
            versao_arquivo = self.identificar_versao_arquivo(linhas)
            codigo_registro = self.identificar_codigo_registro(linha)
            if versao_arquivo != '001':
                logging.warning(f'Poderá ocorrer erro seguinte por problema de versão do arquivo! Versão do arquivo [{versao_arquivo}] não identificada')
            
            if codigo_registro == 'DETALHE':
                dados.append(self.leitura_detalhe(tipo_arquivo, linha))
            elif codigo_registro == 'TRAILER':
                dados.append(self.leitura_trailer(tipo_arquivo, linha))
            elif codigo_registro == 'HEADER' or codigo_registro == '':
                dados.append(self.leitura_header(tipo_arquivo, linha))
            else:
                raise Exception(f'Erro ao realizar a leitura! Código de Registro [{codigo_registro}] não identificado.')
        return dados
            
    def leitura_header(self, tipo_arquivo: str, linha: str, versao_arquivo: str = "001") -> dict:
        """Efetua a leitura do header

        Args:
            versao_arquivo (str): versão do layout CNAB750
            tipo_arquivo (str): tipo 'remessa' ou tipo 'retorno'
            linha (str): dados da linha

        Returns:
            dict: dados do header
        """
        if versao_arquivo == '001' and tipo_arquivo == 'retorno':
            dict_dados = {'tipo_de_registro':self.extrair_campo(linha, 0, 0),
                        'codigo_de_retorno':self.extrair_campo(linha, 1, 1),
                        'literal_de_retorno':self.extrair_campo(linha, 2, 9),
                        'codigo_do_servico':self.extrair_campo(linha, 9, 11),
                        'literal_de_servico':self.extrair_campo(linha, 11, 26),
                        'ispb_participante':self.extrair_campo(linha, 26, 34),
                        'codigo_de_inscricao':self.extrair_campo(linha, 34, 36),
                        'cpf_cnpj':self.extrair_campo(linha, 36, 50),
                        'agencia':self.extrair_campo(linha, 50, 54),
                        'conta':self.extrair_campo(linha, 54, 74),
                        'tipo_conta':self.extrair_campo(linha, 74, 78),
                        'chave_pix':self.extrair_campo(linha, 78, 155),
                        'data_de_geracao':self.extrair_campo(linha, 155, 163),
                        'codigo_do_convenio':self.extrair_campo(linha, 163, 193),
                        'exclusivo_psp_recebedor':self.extrair_campo(linha, 193, 253),
                        'codigos_de_erro':self.extrair_campo(linha, 253, 283),
                        'brancos':self.extrair_campo(linha, 283, 741),
                        'versao_do_arquivo':self.extrair_campo(linha, 741, 744),
                        'numero_sequencial_do_arquivo':self.extrair_campo(linha, 744, 750)}
        return dict_dados
    
    def leitura_detalhe(self, tipo_arquivo: str, linha: str, versao_arquivo: str = "001") -> dict:
        """Efetua a leitura do detalhe

        Args:
            versao_arquivo (str): versão do layout CNAB750
            tipo_arquivo (str): tipo 'remessa' ou tipo 'retorno'
            linha (str): dados da linha

        Returns:
            dict: dados do detalhe
        """
        if versao_arquivo == '001' and tipo_arquivo == 'retorno':
            dict_dados = {'tipo_de_registro':self.extrair_campo(linha, 0, 0),
                        'ispb_participante':self.extrair_campo(linha, 1, 9),
                        'codigo_de_inscricao':self.extrair_campo(linha, 9, 11),
                        'cpf_cnpj':self.extrair_campo(linha, 11, 25),
                        'agencia':self.extrair_campo(linha, 25, 29),
                        'conta':self.extrair_campo(linha, 29, 49),
                        'tipo_conta':self.extrair_campo(linha, 49, 53),
                        'chave_pix':self.extrair_campo(linha, 53, 130),
                        'tipo_cobranca':self.extrair_campo(linha, 130, 130),
                        'cod_do_movimento':self.extrair_campo(linha, 131, 133),
                        'data_do_movimento':self.extrair_campo(linha, 133, 141),
                        'identificador':self.extrair_campo(linha, 141, 176),
                        'expiracao':self.extrair_campo(linha, 176, 191),
                        'data_de_vencimento':self.extrair_campo(linha, 191, 199),
                        'valor_original':self.extrair_campo(linha, 199, 216),
                        'valor_juros':self.extrair_campo(linha, 216, 233),
                        'valor_multa':self.extrair_campo(linha, 233, 250),
                        'valor_desconto_abatimento':self.extrair_campo(linha, 250, 267),
                        'valor_final':self.extrair_campo(linha, 267, 284),
                        'valor_pago':self.formata_valor(self.extrair_campo(linha, 284, 301), 2),
                        'tarifa_de_cobranca':self.extrair_campo(linha, 301, 318),
                        'codigo_de_inscricao_devedor':self.extrair_campo(linha, 318, 320),
                        'cpf_cnpj_devedor':self.extrair_campo(linha, 320, 334),
                        'mensagem_pagador_final':self.extrair_campo(linha, 334, 474),
                        'codigo_de_inscricao_pagador_final':self.extrair_campo(linha, 474, 476),
                        'cpf_cnpj_pagador_final':self.extrair_campo(linha, 476, 490),
                        'nome_pagador_final':self.extrair_campo(linha, 490, 630),
                        'cod_de_liquidacao':self.extrair_campo(linha, 630, 632),
                        'end_to_end_id':self.extrair_campo(linha, 632, 667),
                        'codigos_de_erro':self.extrair_campo(linha, 667, 697),
                        'brancos':self.extrair_campo(linha, 697, 744),
                        'numero_sequencial':self.extrair_campo(linha, 744, 750)}
        return dict_dados

    def leitura_trailer(self, tipo_arquivo: str, linha: str, versao_arquivo: str= "001") -> dict:
        """Efetua a leitura do trailer

        Args:
            versao_arquivo (str): versão do layout CNAB750
            tipo_arquivo (str): tipo 'remessa' ou tipo 'retorno'
            linha (str): dados da linha

        Returns:
            dict: dados do trailer
        """
        if versao_arquivo == '001' and tipo_arquivo == 'retorno':
            dict_dados = {'tipo_de_registro':self.extrair_campo(linha, 0, 0),
                        'codigo_de_retorno':self.extrair_campo(linha, 1, 1),
                        'codigo_de_servico':self.extrair_campo(linha, 2, 4),
                        'ispb':self.extrair_campo(linha, 4, 12),
                        'codigos_de_erro':self.extrair_campo(linha, 12, 42),
                        'brancos':self.extrair_campo(linha, 42, 729),
                        'qtde_de_detalhes':self.extrair_campo(linha, 729, 744),
                        'numero_sequencial':self.extrair_campo(linha, 745, 750)}
        return dict_dados
    
    def formata_valor(self, valor: str, qtd_decimais: int) -> str:
        """Formata um valor para eliminar os zeros a esquerda e inserir a vírgula para marcação dos decimais.

        Args:
            valor (str): valor a ser formatado
            qtd_decimais (int): quantidade de decimais

        Returns:
            str: valor formatado
        """
        valor_sem_zero_esquerda = valor.lstrip('0')
        return valor_sem_zero_esquerda[:-qtd_decimais] + "," + valor_sem_zero_esquerda[-qtd_decimais:]
