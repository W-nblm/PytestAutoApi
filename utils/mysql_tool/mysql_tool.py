import pymysql
from utils.logging_tool.log_control import INFO, ERROR


class MysqlTool:
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            ERROR.logger.error(f"Failed to connect to MySQL: {e}")
            raise

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
            INFO.logger.info(f"Successfully query SQL: {sql}, data: {data}")
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
            INFO.logger.info(f"Successfully executed SQL: {sql}, data: {data}")
            return data
        except AttributeError:
            ERROR.logger.error("MySQL connection not established")
            self.conn.rollback()
            raise


if __name__ == "__main__":
    mysql_tool = MysqlTool(
        host="47.107.113.31",
        user="iot_test",
        port=13306,
        password="DPbbkXGvauYD38uY",
        database="lzyiot",
    )
    data = mysql_tool.query(
        "select au.user_uid FROM app_user au WHERE au.email = '834532523@qq.com' AND au.reg_app_source = 'WObird'"
    )
    print(data)
