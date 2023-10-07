from enum import Enum, unique
from datetime import datetime
from mongoengine import DateTimeField, StringField, Document, EnumField, FloatField, IntField, ListField, BinaryField


class Feriado(Document):

    descricao_feriado = StringField(required=True)
    data_feriado = DateTimeField(required=True)
    dia_semana = StringField(required=True)
    data_inclusao = DateTimeField(default=datetime.now())

    meta = {'collection': 'febrabanHoliday', 'db_alias': 'CoeRpa'}
