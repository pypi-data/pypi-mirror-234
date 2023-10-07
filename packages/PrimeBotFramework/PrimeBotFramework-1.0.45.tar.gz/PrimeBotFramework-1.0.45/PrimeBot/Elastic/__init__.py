from datetime import datetime
from elasticsearch_dsl import Document, Date, Keyword, connections, \
    Integer


class BaseDocument(Document):
    timestamp = Date(default_timezone='Brazil/East')
    robot_name = Keyword()

    @classmethod
    def connect(cls, host, user, pwd):
        connections.create_connection(hosts=[host], http_auth=f'{user}:{pwd}')


class RobotLog(BaseDocument):
    message = Keyword()
    level = Keyword()

    class Index:
        name = 'robot-logs'
        settings = {
            "number_of_shards": 1
        }

    def save(self, **kwargs):
        if not self.timestamp:
            self.timestamp = datetime.now()

        kwargs['index'] = self.timestamp.strftime(
            f'robot-logs-{self.robot_name}-%Y.%m')
        return super().save(**kwargs)


class SuiteLog(BaseDocument):
    status = Keyword()
    duration = Integer()

    class Index:
        name = 'robot-suite'
        settings = {
            "number_of_shards": 1
        }

    def save(self, **kwargs):
        if not self.timestamp:
            self.timestamp = datetime.now()

        kwargs['index'] = self.timestamp.strftime(
            f'robot-suite-{self.robot_name}-%Y.%m')
        return super().save(**kwargs)



