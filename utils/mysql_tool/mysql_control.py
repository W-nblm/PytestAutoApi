import ast
import datetime
import decimal
from warnings import filterwarnings
import pymysql
from typing import List, Union, Text, Dict
from utils import config
from utils.logging_tool.log_control import ERROR
from utils.read_files_tool.regular_control import sql_regular
from utils.read_files_tool.regular_control import cache_regular
from utils.other_tools.exceptions import DataAcquisitionFailed, ValueTypeError
from utils.logging_tool.log_control import INFO


class MySqlDB:

    if config.mysql_db.switch:

        def __init__(self):
            try:
                self.conn = pymysql.connect(
                    host=config.mysql_db.host,
                    user=config.mysql_db.user,
                    password=config.mysql_db.password,
                    port=config.mysql_db.port,
                    database=config.mysql_db.database,
                )
                self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
                INFO.logger.info(f"Connected Successfully to MySQL,conn:{self.conn}")
            except Exception as e:
                ERROR.logger.error(f"Failed to connect to MySQL: {e}")

        def __del__(self):
            try:
                self.cursor.close()
                self.conn.close()
                INFO.logger.info(f"MySQL connection closed successfully")
            except Exception as e:
                ERROR.logger.error(f"Failed to close MySQL connection: {e}")

        def query(self, sql, state="all"):
            """
            :param sql: SQL statement
            :param state: 'all' or 'one'
            :return:
            """
            try:
                self.cursor.execute(sql)
                if state == "all":
                    data = self.cursor.fetchall()
                elif state == "one":
                    data = self.cursor.fetchone()
                else:
                    raise ValueError("Invalid state parameter")
                return data
            except Exception as e:
                ERROR.logger.error(f"Failed to execute SQL: {e}")

        def execute(self, sql):
            """
            :param sql: SQL statement
            :return:
            """
            try:
                data = self.cursor.execute(sql)
                self.conn.commit()
                return data
            except AttributeError:
                ERROR.logger.error("MySQL connection not established")
                self.conn.rollback()
                raise

        @classmethod
        def sql_data_handler(cls, query_result, data):
            """
            处理sql查询出的数据格式"
            :param query_result: 查询结果
            :param data: 传入的数据
            :return:
            """
            for key, value in query_result.items():
                if isinstance(value, decimal.Decimal):
                    data[key] = float(value)
                elif isinstance(value, datetime.datetime):
                    data[key] = str(value)
                else:
                    data[key] = value
            return data


class SetUpMySQL(MySqlDB):
    """处理前置sql"""

    def setup_sql_data(self, sql: Union[List, None]) -> Dict:
        """
        处理前置sql
        :param sql: 前置sql
        :return:
        """
        sql = ast.literal_eval(cache_regular(str(sql)))
        try:
            data = {}
            if sql is not None:
                for i in sql:
                    # 判断sql查询类型
                    if i.startswith("select"):
                        sql_data = self.query(sql=i)[0]
                        for key, value in sql_data.items():
                            data[key] = value
                    else:
                        self.execute(sql=i)
            return data
        except Exception as e:
            raise DataAcquisitionFailed(f"Failed to set up MySQL data: {e}")


class AssertExecution(MySqlDB):
    """断言执行"""

    def assert_execution(self, sql: list, resp) -> dict:
        """
        断言执行
        :param sql: 断言sql
        :param resp: 接口响应数据
        """
        try:
            if isinstance(sql, list):
                data = {}
                _sql_type = ["UPDATE", "update", "DELETE", "delete", "INSERT", "insert"]
                if any(i in sql for i in _sql_type) is False:
                    for i in sql:
                        sql = sql_regular(i, resp)
                        if sql is not None:
                            query_result = self.query(sql=sql)[0]
                            data = self.sql_data_handler(query_result, data)
                        else:
                            raise DataAcquisitionFailed(
                                f"未查询到数据,请检查sql语句,sql语句为:{sql}"
                            )
                else:
                    raise DataAcquisitionFailed(
                        f"sql语句类型错误,请检查sql语句,sql语句为:{sql}"
                    )
                return data
        except Exception as e:
            ERROR.logger.error(f"Failed to assert execution: {e}")
            raise e

        if __name__ == "__main__":
            mysql = MySqlDB()
            b = mysql.query("select * from user")
            print(b)
