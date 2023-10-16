"""This Module will give access to MySQL in our Environment"""
from dataclasses import dataclass
import time
import logging
import socket
import mysql.connector as mc
from werkzeug import datastructures as ds
from .credauth import cred
from .common import DefaultDict, send_push_message

@dataclass
class Mysql(DefaultDict):
    """Control MySQL

    Args:
        DefaultDict (_type_): _description_
    """    
    sql: str | None =  None
    dst: str | None = None
    host: str | None = None
    req: ds.MultiDict | None = None
    status: int = 500
    status_code: int = 500
    failure: str = ""
    runtime: float = -1

    def __post_init__(self):
        start = time.time()
        self.get_Credentials()
        self.check_Connection()
        end = time.time()
        self.runtime = round(end - start, 2)

    def get_Credentials(self) -> bool:
        try:
            row = cred('mysql')
            self.__host = "localhost"
            self.__pwd, self.__user, self.__db = row['password'], row['username'], row['devtype']
            self.status = 200
            return True
        except Exception as e:
            self.failure = f"get_Credentials failed with {e}"
            self.status = 500
            return False

    def check_Connection(self) -> None:
        try:
            if self.__connection.is_connected() is not True:
                self.__connection.connect()
                if self.__connection.is_connected() is True:
                    self.cursor = self.__connection.cursor(buffered=True)
                    self.status = 200
                    logging.info("Reconnect MySQL Connection.")
        except Exception as e:
            self.__connection = mc.connect (host = self.__host,
                                            user = self.__user,
                                            passwd = self.__pwd,
                                            db = self.__db)
            self.cursor = self.__connection.cursor(buffered=True)
            self.status = 200
            logging.info("Establish MySQL Connection.")


    def get_slave_status(self) -> None:
        try:
            self.check_Connection()
            self.host = socket.gethostname()
            result = self.cursor.execute("show slave status")
            result = self.cursor.fetchall()
            Slave_IO_Running = result[0][10]
            Slave_SQL_Running = result[0][11]
            Last_Error = result[0][19]
            #print(Slave_IO_Running, Slave_SQL_Running, Last_Error)
            #print(type(Slave_IO_Running), type(Slave_SQL_Running), type(Last_Error))

            if Slave_IO_Running != "Yes" and Slave_SQL_Running != "Yes" and Last_Error != "":
                self.status = 500
                self.failure = (f"MySQL {self.host} Slave_IO_Running = {Slave_IO_Running} Slave_SQL_Running = {Slave_SQL_Running} Last_Error = {Last_Error}")
                send_push_message(topic="Zuhause_Alerts", title="{host} - Mariadb Slave not running", prio="urgent", data = f"{self.host} - Slave_IO_Running = {Slave_IO_Running} Slave_SQL_Running = {Slave_SQL_Running} Last_Error = {Last_Error}" )
            else:
                self.status = 200
                # test entry, to prove it is working in good condition
                #send_push_message(topic="Zuhause_Alerts", title="Mariadb Slave not running", prio="urgent", data = f"Slave_IO_Running = {Slave_IO_Running} Slave_SQL_Running = {Slave_SQL_Running} Last_Error = {Last_Error}")

        except Exception as e:
            self.failure = (f"Exception in get_slave_status with {e}")
            self.status = 500
            logging.error(f"Exception in get_slave_status with {e}")

    def select(self, sql=None, dst='sql'):
        try:
            if sql is not None and isinstance(sql, str):
                self.sql = sql
            self.check_Connection()
            cursor = self.__connection.cursor()
            cursor.execute(sql)
            self.__result = cursor.fetchall()
            #return self.__result
        except mc.Error as e:
            cursor.close()
            self.__connection.close()
            logging.error("%d: %s" % (e.args[0], e.args[1]))
            return 'MySQL Query was not successful'
        cursor.close()
        self.__connection.close()
        if self.__result == []:
            return 'empty set'
        else:
            #return str(result[0])
            if dst == 'http':
                return ','.join([str(i) for i in self.__result[0]])
            elif dst == 'http2':
                return ','.join([str(i) for i in self.__result])
            elif dst == 'normal' or dst == 'sql':
                return self.__result
            else:
                return self.__result[0]
            #return result

    def select_temp(self, what=None, dst='sql'):
        try:
            if what is not None and isinstance(what, str):
                self.sql = what
            self.check_Connection()
            cursor = self.__connection.cursor()
            cursor.execute(what)
            self.__result = cursor.fetchall()
            #return self.__result
        except mc.Error as e:
            cursor.close()
            self.__connection.close()
            logging.error("%d: %s" % (e.args[0], e.args[1]))
            return 'MySQL Query was not successful'
        cursor.close()
        self.__connection.close()
        if self.__result == []:
            return 'empty set'
        else:
            #return str(result[0])
            if dst == 'http':
                return ','.join([str(i) for i in self.__result[0]])
            elif dst == 'http2':
                return ','.join([str(i) for i in self.__result])
            elif dst == 'normal' or dst == 'sql':
                return self.__result
            else:
                return self.__result[0]

    def update(self, sql=None):
        try:
            if sql is not None and isinstance(sql, str):
                self.sql = sql
            self.check_Connection()
            cursor = self.__connection.cursor()
            cursor.execute(sql)
        except mc.Error as e:
            self.__connection.rollback()
            cursor.close()
            self.__connection.close()
            logging.error("Error %d: %s" % (e.args[0], e.args[1]))
            return 'MySQL commit was not successful'
        self.__connection.commit()
        cursor.close()
        self.__connection.close()
        return 'success'

    def updatemore(self, sqlinsert, records):
        rowcount=0
        try:
            if sqlinsert is not None and isinstance(sqlinsert, str):
                self.sql = sql
            self.check_Connection()
            cursor = self.__connection.cursor()
            for e in records:
                sql = sqlinsert.format(name=e[0], ga1=e[1], data=e[2])
                cursor.execute(sql)
        except mc.Error as e:
            self.__connection.rollback()
            cursor.close()
            self.__connection.close()
            logging.error("Error %d: %s" % (e.args[0], e.args[1]))
            return 'MySQL commit was not successful'
        self.__connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        self.__connection.close()
        return rowcount
