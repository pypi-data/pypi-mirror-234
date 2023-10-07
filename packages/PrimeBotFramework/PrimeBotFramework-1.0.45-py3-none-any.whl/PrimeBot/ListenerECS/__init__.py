import logging
import ecs_logging

class ListenerECS:
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self, aplication_name='app', filename='log.json'):
        self.ROBOT_LIBRARY_LISTENER = self
        self.logger = logging.getLogger(aplication_name)
        self.logger.setLevel(level=logging.NOTSET)
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(ecs_logging.StdlibFormatter(
            exclude_fields=["log.origin", "log.original", "process"]))
        self.logger.addHandler(file_handler)
        self.logger.info(msg="Logger Initialized")

    def start_suite(self, name: str, attrs: dict):
        """Listener Function"""
        self.logger.info(
            msg=f"name: {name} | doc: {attrs['doc']} | starttime: {attrs['starttime']} | trigger_type: start_suite"
        )

    def start_test(self, name: str, attributes: dict):
        """Listener Function"""
        self.logger.info(
            msg=f"name: {name} | doc: {attributes['doc']} | starttime: {attributes['starttime']} | trigger_type: start_task"
        )

    def start_keyword(self, name: str, attributes: dict):
        """Listener Function"""
        message = f"name: {name} | doc: {attributes['doc']} | type: {attributes['type']} | starttime: {attributes['starttime']} | trigger_type: start_keyword"
        
        # Atributos adicionais apenas funcionam no RF 6.0
        # if attributes['type'] == 'FOR':
        #     message += f" | variables: {attributes['variables']} | flavor: {attributes['flavor']} | values: {attributes['values']}"
        
        # elif attributes['type'] == 'ITERATION':
        #     message += f" | variables: {attributes['variables']}"

        # elif attributes['type'] == 'WHILE' or attributes['type'] == 'IF' or attributes['type'] == 'ELSE_IF':
        #     message += f" | condition: {attributes['condition']}"
        
        # elif attributes['type'] == 'EXCEPT':
        #     message += f" | variable: {attributes['variable']}"

        self.logger.info(
            msg=message
        )

    def log_message_extra(self, **kwargs):
        message = {}
        extras = {}
        for key, value in kwargs.items():
            if key == 'message' or key == 'level':
                message[key] = value
            else:
                extras[key] = value
        
        self.log_message(message=message, extras=extras)

    def log_message(self, message: dict, extras={}):
        """Listener Function"""
        self.__log_with_level(f"message: {message['message']}", message['level'], extras)

    def end_keyword(self, name: str, attributes: dict):
        """Listener Function"""
        message = f"name: {name} | type: {attributes['type']} | endtime: {attributes['endtime']} | elapsedtime: {attributes['elapsedtime']} | status: {attributes['status']} | trigger_type: end_keyword"

        if attributes['status'] == 'FAIL':
            message += f" | lineno: {attributes['lineno']}"

        self.__log_with_level(msg=message, status=attributes['status'])

    def end_test(self, name: str, attributes: dict):
        """Listener Function"""

        message = f"name: {name} | endtime: {attributes['endtime']} | elapsedtime: {attributes['elapsedtime']} | status: {attributes['status']} | sys_message: {attributes['message']} | trigger_type: end_task"
        self.__log_with_level(msg=message, status=attributes['status'])

    def end_suite(self, name: str, attributes: dict):
        """Listener Function"""
        message = f"name: {name} | endtime: {attributes['endtime']} | elapsedtime: {attributes['elapsedtime']} | status: {attributes['status']} | statistics: {attributes['statistics']} | sys_message: {attributes['message']} | trigger_type: end_suite"
        self.__log_with_level(msg=message, status=attributes['status'])

    def __log_with_level(self, msg, status, extra={}):
        
        if status == 'FAIL' or status == 'ERROR':
            self.logger.error(msg=msg,extra=extra)
        else:
            self.logger.info(msg=msg, extra=extra)
        
