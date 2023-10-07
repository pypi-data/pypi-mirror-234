import cx_Oracle



class OracleDB:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    def __init__(self, dir_instant_client="C:\\oracle\\instantclient"):
        cx_Oracle.init_oracle_client(lib_dir=dir_instant_client)

    def execute_query(self, user, password, dsn, encoding, query):
        with cx_Oracle.connect(user=user, password=password,
                               dsn=dsn,
                               encoding=encoding) as connection:
            cur = connection.cursor()
            cur.execute(query)
            res = cur.fetchall()
        return res