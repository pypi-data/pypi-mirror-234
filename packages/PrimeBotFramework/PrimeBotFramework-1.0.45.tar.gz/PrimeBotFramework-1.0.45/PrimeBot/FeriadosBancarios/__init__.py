from PrimeBot.FeriadosBancarios.model import Feriado
import datetime


class FeriadosBancarios():


    def consultar_feriado(self, data_feriado):
        """Consulta se uma data está no banco de dados. Caso a data esteja registrada como feriado, retorna True, caso contrario False.

        Args:
            data_feriado (str):  data no formato dd/MM/yyyy. Ex: 01/12/2023

        Returns:
            boolean: data é feriado

        """
        data_feriado_datetime = datetime.datetime.strptime(data_feriado, '%d/%m/%Y')
        if list(Feriado.objects(data_feriado=data_feriado_datetime)):
            return True
        else:
            return False
        
    import datetime

    def consultar_dias_da_semana(self, ano, mes):
        """Consulta os dias da semana de mês do ano

        Args:
            ano (int): mes correspondente
            mes (int): ano correspondente

        Returns:
            list: lista com os dias da semana do mês do ano no formato dd/MM/yyyy
        """
        inicio_mes = datetime.date(ano, mes, 1)
        fim_mes = datetime.date(ano, mes + 1, 1) if mes < 12 else datetime.date(ano + 1, 1, 1)
        dias_da_semana = []

        dia_atual = inicio_mes
        while dia_atual < fim_mes:
            if dia_atual.weekday() < 5:
                dias_da_semana.append(dia_atual.strftime('%d/%m/%Y'))
            dia_atual += datetime.timedelta(days=1)

        return dias_da_semana


    def consultar_dias_uteis_do_mes(self, ano, mes):
        """Consulta os dias uteis de um mês do ano

        Args:
            ano (int): mes correspondente
            mes (int): ano correspondente

        Returns:
            list: lista com os dias uteis do mês do ano no formato dd/MM/yyyy
        """
        dias_da_semana = self.consultar_dias_da_semana(ano, mes)
        dias_uteis = [x for x in dias_da_semana if not self.consultar_feriado(x)]
        return dias_uteis
