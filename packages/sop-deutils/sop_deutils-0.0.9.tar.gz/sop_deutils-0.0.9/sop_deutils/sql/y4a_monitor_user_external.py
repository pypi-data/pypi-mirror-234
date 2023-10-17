import datetime
import logging
import pytz
import warnings
import pandas as pd
from psycopg2 import connect
from ..y4a_retry import retry_on_error
from ..y4a_credentials import get_credentials

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

warnings.filterwarnings("ignore", category=UserWarning)


class MonitorUserExternal:
    def __init__(
        self,
        conn_username: str,
        conn_password: str,
        conn_host: str,
        conn_db: str,
        conn_number: int,
    ) -> None:
        self.conn_username = conn_username
        self.conn_password = conn_password
        self.conn_host = conn_host
        self.conn_db = conn_db
        self.conn_number = conn_number

        self.log_conn_df = pd.DataFrame(
            {
                'time_conn': str(
                    datetime.datetime.now(
                        pytz.timezone('Asia/Ho_Chi_Minh'),
                    ).replace(microsecond=0).replace(tzinfo=None)
                ),
                'host': self.conn_host,
                'username': self.conn_username,
                'password': self.conn_password,
                'database': self.conn_db,
                'num_conn': self.conn_number,
            },
            index=[0],
        )

        self.id_conn = None

    @retry_on_error(max_retries=5)
    def open_conn(self) -> None:
        self.credentials = get_credentials(
            platform='pg',
            account_name='da_admin',
        )
        self.conn = connect(
            user=self.credentials['user_name'],
            password=self.credentials['password'],
            host='172.30.12.153',
            port=5432,
            database='serving',
        )

    def close_conn(self) -> None:
        self.conn.close()

    def execute(
        self,
        sql: str,
        fetch_output: bool = False,
    ) -> list | None:
        output = None

        cur = self.conn.cursor()

        cur.execute(sql)

        if fetch_output:
            output = cur.fetchall()

        cur.close()
        self.conn.commit()

        return output

    def generate_log_conn(self) -> None:
        sql = "INSERT INTO metadata.monitor_user_sql_connection "
        sql += "(time_conn, host, username, password, database, num_conn) "
        sql += f"VALUES ('{self.log_conn_df['time_conn'].values[0]}', "
        sql += f"'{self.log_conn_df['host'].values[0]}', "
        sql += f"'{self.log_conn_df['username'].values[0]}', "
        sql += f"'{self.log_conn_df['password'].values[0]}', "
        sql += f"'{self.log_conn_df['database'].values[0]}', "
        sql += f"{self.log_conn_df['num_conn'].values[0]}) "
        sql += "RETURNING id_conn"

        self.id_conn = self.execute(
            sql=sql,
            fetch_output=True,
        )[0][0]

    def update_log_conn(self) -> None:
        sql = "UPDATE metadata.monitor_user_sql_connection SET "
        sql += "is_closed = 1 WHERE "
        sql += f"id_conn = {self.id_conn} "
        sql += f"AND time_conn = '{self.log_conn_df['time_conn'].values[0]}' "
        sql += f"AND host = '{self.log_conn_df['host'].values[0]}' "
        sql += f"AND username = '{self.log_conn_df['username'].values[0]}' "

        self.execute(sql)
