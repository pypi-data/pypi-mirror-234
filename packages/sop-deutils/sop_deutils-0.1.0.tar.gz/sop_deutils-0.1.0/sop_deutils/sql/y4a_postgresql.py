import logging
import datetime
import warnings
from typing import Callable
import pandas as pd
from psycopg2 import pool, connect
from io import StringIO
from .y4a_monitor_user_external import MonitorUserExternal
from ..y4a_retry import retry_on_error
from ..y4a_credentials import get_credentials


warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class PostgreSQLUtils:
    """
    Utils for PostgreSQL

    :param account_name: the client account name to connect to PostgreSQL
    :param db_host: host db name to connect
    :param db: PostgreSQL database to connect
        defaults to 'serving'
    """

    def __init__(
        self,
        account_name: str,
        db_host: str,
        db: str = 'serving',
    ) -> None:
        self.hosts = {
            'raw_master': '172.30.12.153',
            'raw_repl': '172.30.12.154',
            'serving_master': '172.30.12.153',
            'serving_repl': '172.30.12.154',
        }
        self.account_name = account_name
        self.credentials = get_credentials(
            platform='pg',
            account_name=self.account_name,
        )
        self.db_user = self.credentials['user_name']
        self.db_password = self.credentials['password']
        self.db_host = db_host
        self.host = self.hosts[self.db_host]
        self.db = db

    @retry_on_error(max_retries=5)
    def create_pool_conn(
        self,
        pool_size: int = 1,
    ) -> Callable:
        """
        Create a connection pool to connect to PostgreSQL

        :param pool_size: number of connections in the pool

        :return: connection pool contains multiple connections
            to the database
        """

        db_pool_conn = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=pool_size,
            user=self.db_user,
            password=self.db_password,
            host=self.host,
            port=5432,
            database=self.db,
        )
        self.generate_log_conn(pool_size)

        return db_pool_conn

    def close_pool_conn(
        self,
        db_pool_conn: Callable,
    ) -> None:
        """
        Close and remove the connection pool

        :param db_pool_conn: connection pool contains multiple connections
            to the database
        """

        self.update_log_conn()
        db_pool_conn.closeall()

    @retry_on_error(max_retries=5)
    def open_conn(self) -> Callable:
        """
        Create a new connection to PostgreSQL

        :return: connection object to connect to database
        """

        conn = connect(
            user=self.db_user,
            password=self.db_password,
            host=self.host,
            port=5432,
            database=self.db,
        )

        return conn

    def close_conn(
        self,
        conn: Callable,
    ) -> None:
        """
        Close the connection to PostgreSQL

        :param conn: connection object to connect to database
        """

        conn.close()

    def generate_log_conn(
        self,
        conn_number: int,
    ) -> None:
        try:
            self.external_monitor = MonitorUserExternal(
                conn_username=self.db_user,
                conn_password=self.db_password,
                conn_host=self.host,
                conn_db=self.db,
                conn_number=conn_number,
            )
            self.external_monitor.open_conn()
            self.external_monitor.generate_log_conn()
        except Exception as e:
            logging.error('Can not track log for this connection')
            logging.error(e)

    def update_log_conn(self) -> None:
        try:
            self.external_monitor.update_log_conn()
            self.external_monitor.close_conn()
        except Exception as e:
            logging.error('Can not update log for this connection')
            logging.error(e)

    def _serialize_cell(
        self,
        cell,
    ) -> str:
        if cell is None:
            return None
        if isinstance(cell, datetime.datetime):
            return cell.isoformat()

        return str(cell)

    def read_sql_file(
        self,
        sql_file_path: str,
    ) -> str:
        """
        Get the SQL query given by SQL file

        :param sql_file_path: the located path of SQL file

        :return: SQL query
        """

        with open(sql_file_path, 'r') as file:
            sql = file.read()

        return sql

    def insert_data(
        self,
        data: pd.DataFrame,
        schema: str,
        table: str,
        commit_every: int = 1000,
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Insert data to PostgreSQL table

        :param data: a dataframe contains data to insert
        :param schema: schema contains table to insert
        :param table: table name to insert
        :param commit_every: number rows of data to commit each time
            defaults to 1000
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        if not db_pool_conn:
            conn = self.open_conn()
        else:
            conn = db_pool_conn.getconn()

        try:
            cur = conn.cursor()

            target_fields = data.columns.to_list()
            target_fields = ", ".join(target_fields)
            target_fields = "({})".format(target_fields)

            rows = [
                tuple(r) for r in data.to_numpy()
            ]

            for i, row in enumerate(rows, 1):
                lst = []
                for cell in row:
                    lst.append(self._serialize_cell(cell))
                values = tuple(lst)
                placeholders = ["%s", ] * len(values)
                sql = "INSERT INTO "
                sql += "{0} {1} VALUES ({2})".format(
                    f'{schema}.{table}',
                    target_fields,
                    ",".join(placeholders)
                )
                cur.execute(sql, values)
                if i % commit_every == 0:
                    conn.commit()
                    logging.info(
                        f"Loaded {i} into {table} rows so far"
                    )

            cur.close()
            conn.commit()

            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)

            logging.info(
                f"Done loading. Loaded a total of {i} rows"
            )
        except Exception as e:
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
            raise e

    def bulk_insert_data(
        self,
        data: pd.DataFrame,
        schema: str,
        table: str,
        commit_every: int = 1000,
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Insert data to PostgreSQL table using COPY method
            (using when the data to insert is large)

        :param data: a dataframe contains data to insert
        :param schema: schema contains table to insert
        :param table: table name to insert
        :param commit_every: number rows of data to commit each time
            defaults to 1000
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        if len(data) == 0:
            return

        if not db_pool_conn:
            conn = self.open_conn()
        else:
            conn = db_pool_conn.getconn()

        try:
            cur = conn.cursor()

            columns = list(data.columns)

            data_chunk = [
                data[i:i+commit_every]
                for i in range(
                    0,
                    len(data),
                    commit_every,
                )
            ]

            for chunk in data_chunk:
                output = StringIO()
                chunk.to_csv(
                    output,
                    sep='|',
                    header=False,
                    index=False,
                )
                output.seek(0)

                copy_sql = f"COPY {schema}.{table} ({', '.join(columns)}) "
                copy_sql += "FROM stdin WITH CSV DELIMITER as '|'"

                cur.copy_expert(sql=copy_sql, file=output)
                conn.commit()
                logging.info(
                    f'Loaded {commit_every} into {table} rows so far'
                )

            cur.close()
            conn.commit()
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)

            logging.info(
                f"Done loading. Loaded a total of {len(data)} rows"
            )
        except Exception as e:
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
            raise e

    def upsert_data(
        self,
        data: pd.DataFrame,
        schema: str,
        table: str,
        primary_keys: list,
        commit_every: int = 1000,
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Upsert data (update the row if it already exist when inserting)
            to PostgreSQL table

        :param data: a dataframe contains data to upsert
        :param schema: schema contains table to upsert
        :param table: table name to upsert
        :param primary_keys: list of primary keys of the table
        :param commit_every: number rows of data to commit each time
            defaults to 1000
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        if not db_pool_conn:
            conn = self.open_conn()
        else:
            conn = db_pool_conn.getconn()

        try:
            cur = conn.cursor()

            target_fields = data.columns.to_list()
            target_fields = ", ".join(target_fields)
            target_fields = "({})".format(target_fields)

            to_update_columns = [
                col for col in data.columns
                if col not in primary_keys
            ]
            to_update_columns_sql = list()
            for col in to_update_columns:
                to_update_columns_sql.append(
                    f"{col} = excluded.{col}"
                )

            rows = [
                tuple(r) for r in data.to_numpy()
            ]

            for i, row in enumerate(rows, 1):
                lst = []
                for cell in row:
                    lst.append(self._serialize_cell(cell))
                values = tuple(lst)
                placeholders = ["%s", ] * len(values)
                sql = "INSERT INTO "
                sql += "{0} {1} VALUES ({2})".format(
                    f'{schema}.{table}',
                    target_fields,
                    ",".join(placeholders)
                )
                sql += "ON CONFLICT "
                sql += f"({', '.join(primary_keys)}) "
                sql += "DO UPDATE SET "
                sql += f"{', '.join(to_update_columns_sql)}"

                cur.execute(sql, values)
                if i % commit_every == 0:
                    conn.commit()
                    logging.info(
                        f"Loaded {i} into {table} rows so far"
                    )

            cur.close()
            conn.commit()
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)

            logging.info(
                f"Done loading. Loaded a total of {i} rows"
            )
        except Exception as e:
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
            raise e

    def bulk_upsert_data(
        self,
        data: pd.DataFrame,
        schema: str,
        table: str,
        primary_keys: list,
        commit_every: int = 1000,
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Upsert data (update the row if it already exist when inserting)
            to PostgreSQL table using COPY method
            (using when the data to uspert is large)

        :param data: a dataframe contains data to upsert
        :param schema: schema contains table to upsert
        :param table: table name to upsert
        :param primary_keys: list of primary keys of the table
        :param commit_every: number rows of data to commit each time
            defaults to 1000
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        if len(data) == 0:
            return

        if not db_pool_conn:
            conn = self.open_conn()
        else:
            conn = db_pool_conn.getconn()

        try:
            cur = conn.cursor()

            columns = list(data.columns)
            to_update_columns = [
                col for col in columns
                if col not in primary_keys
            ]
            to_update_columns_sql = list()
            for col in to_update_columns:
                to_update_columns_sql.append(
                    f"{col} = excluded.{col}"
                )

            tmp_table = f'tmp_{table}_bulk_upsert'
            create_tmp_table_sql = f"CREATE TEMP TABLE {tmp_table} "
            create_tmp_table_sql += "ON COMMIT DROP "
            create_tmp_table_sql += f"AS SELECT * FROM {schema}.{table} "
            create_tmp_table_sql += "WITH NO DATA"

            data_chunk = [
                data[i:i+commit_every]
                for i in range(
                    0,
                    len(data),
                    commit_every,
                )
            ]

            for chunk in data_chunk:
                cur.execute(create_tmp_table_sql)

                output = StringIO()
                chunk.to_csv(
                    output,
                    sep='|',
                    header=False,
                    index=False,
                )
                output.seek(0)

                copy_sql = f"COPY {tmp_table} ({', '.join(columns)}) "
                copy_sql += "FROM stdin WITH CSV DELIMITER as '|'"

                cur.copy_expert(sql=copy_sql, file=output)

                upsert_data_sql = f"INSERT INTO {schema}.{table} "
                upsert_data_sql += f"(SELECT * FROM {tmp_table}) "
                upsert_data_sql += "ON CONFLICT "
                upsert_data_sql += f"({', '.join(primary_keys)}) "
                upsert_data_sql += "DO UPDATE SET "
                upsert_data_sql += f"{', '.join(to_update_columns_sql)}"

                cur.execute(upsert_data_sql)

                conn.commit()
                logging.info(
                    f'Loaded {commit_every} into {table} rows so far'
                )

            cur.close()
            conn.commit()
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)

            logging.info(
                f"Done loading. Loaded a total of {len(data)} rows"
            )
        except Exception as e:
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
            raise e

    def update_table(
        self,
        data: pd.DataFrame,
        schema: str,
        table: str,
        columns: list,
        primary_keys: list,
        commit_every: int = 1000,
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Update new data of specific columns in the table
            based on primary keys

        :param data: a dataframe contains data to update
            (including primary keys and columns to update)
        :param schema: schema contains table to update data
        :param table: table to update data
        :param columns: list of column names to update data
        :param primary_keys: list of primary keys of table to update data
        :param commit_every: number rows of data to commit each time
            defaults to 1000
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        if len(data) == 0:
            return

        if not db_pool_conn:
            conn = self.open_conn()
        else:
            conn = db_pool_conn.getconn()

        try:
            cur = conn.cursor()

            sql = f"UPDATE {schema}.{table} SET "
            sql += ", ".join(
                [
                    f"{col} = %s" for col in columns
                ]
            )
            sql += " WHERE "
            sql += " AND ".join(
                [
                    f"{key} = %s" for key in primary_keys
                ]
            )

            sub_cols = columns + primary_keys
            rows = [
                tuple(r) for r in data[sub_cols].to_numpy()
            ]

            for i, row in enumerate(rows, 1):
                lst = []
                for cell in row:
                    lst.append(cell)
                values = tuple(lst)
                cur.execute(sql, values)
                if i % commit_every == 0:
                    conn.commit()
                    logging.info(
                        f"Updated {i} to {table} rows so far"
                    )

            cur.close()
            conn.commit()
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)

            logging.info(
                f"Done updating. Updated a total of {i} rows"
            )
        except Exception as e:
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
            raise e

    def get_data(
        self,
        sql: str,
        db_pool_conn: Callable = None,
    ) -> pd.DataFrame:
        """
        Get data from PostgreSQL database given by a SQL query

        :param sql: the SQL query to get data
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used

        :return: dataframe contains data extracted by the given SQL query
        """

        if not db_pool_conn:
            conn = self.open_conn()
        else:
            conn = db_pool_conn.getconn()

        try:
            data = pd.read_sql(
                sql=sql,
                con=conn,
            )

            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)

            return data
        except Exception as e:
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
            raise e

    def select_distinct(
        self,
        col: str,
        schema: str,
        table: str,
        db_pool_conn: Callable = None,
    ) -> list:
        """
        Get the distinct values of a specified column in a PostgreSQL table

        :param col: the column name to get the distinct data
        :param schema: the schema contains table to get data
        :param table: the table to get data
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used

        :return: list of distinct data
        """

        if not db_pool_conn:
            conn = self.open_conn()
        else:
            conn = db_pool_conn.getconn()

        try:
            sql = f"SELECT DISTINCT {col} "
            sql += f"FROM {schema}.{table}"

            data = pd.read_sql(
                sql=sql,
                con=conn,
            )[col].to_list()

            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)

            return data
        except Exception as e:
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
            raise e

    def show_columns(
        self,
        schema: str,
        table: str,
        db_pool_conn: Callable = None,
    ) -> list:
        """
        Get list of columns name of a specific PostgreSQL table

        :param schema: the schema contains table to get columns
        :param table: the table to get columns
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used

        :return: list of column names of the table
        """

        sql = "SELECT column_name "
        sql += "FROM information_schema.columns "
        sql += f"WHERE table_schema = {schema} "
        sql += f"AND table_name = {table}"

        columns = self.get_data(
            sql=sql,
            db_pool_conn=db_pool_conn,
        )['column_name'].to_list()

        return columns

    def execute(
        self,
        sql: str,
        fetch_output: bool = False,
        db_pool_conn: Callable = None,
    ) -> list | None:
        """
        Execute the given SQL query

        :param sql: SQL query to execute
        :param fetch_output: whether to fetch the results of the query
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used

        :return: list of query output if fetch_output is True,
            otherwise None
        """

        if not db_pool_conn:
            conn = self.open_conn()
        else:
            conn = db_pool_conn.getconn()

        output = None

        try:
            cur = conn.cursor()

            cur.execute(sql)

            if fetch_output:
                output = cur.fetchall()

            cur.close()
            conn.commit()
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
        except Exception as e:
            if not db_pool_conn:
                self.close_conn(conn)
            else:
                db_pool_conn.putconn(conn)
            raise e

        return output

    def add_column(
        self,
        schema: str,
        table: str,
        column_name: str | None = None,
        dtype: str | None = None,
        muliple_columns: dict = {},
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Create new column for a specific table

        :param schema: the schema contains table to create column
        :param table: the table to create column
        :param column_name: name of the column to create
            available when creating single column
            defaults to None
        :param dtype: data type of the column to create
            available when creating single column
            defaults to None
        :param muliple_columns: dictionary contains columns name as key
            and data type of columns as value respectively
            defaults to empty dictionary
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        sql = f"ALTER TABLE {schema}.{table} "
        if muliple_columns:
            sql += ", ".join(
                [
                    f"ADD COLUMN IF NOT EXISTS {col} {muliple_columns[col]}"
                    for col in muliple_columns.keys()
                ]
            )
        else:
            sql += f"ADD COLUMN IF NOT EXISTS {column_name} {dtype}"

        self.execute(
            sql=sql,
            db_pool_conn=db_pool_conn,
        )

    def create_table(
        self,
        schema: str,
        table: str,
        columns_with_dtype: dict,
        columns_primary_key: list = [],
        columns_not_null: list = [],
        columns_with_default: dict = {},
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Create new table in the database

        :param schema: schema contains table to create
        :param table: table name to create
        :param columns_with_dtype: dictionary contains column names
            as key and the data type of column as value respectively
        :param columns_primary_key: list of columns to set primary keys
            defaults to empty list
        :param columns_not_null: list of columns to set constraints not null
            defaults to empty list
        :param columns_with_default: dictionary contains column names
            as key and the default value of column as value respectively
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        cols_sql = list()
        for col in columns_with_dtype.keys():
            col_sql = f"{col} {columns_with_dtype[col]}"
            if col in columns_not_null:
                col_sql += " NOT NULL"
            if col in columns_with_default.keys():
                if isinstance(columns_with_default[col], str):
                    default_value = f"'{columns_with_default[col]}'"
                else:
                    default_value = columns_with_default[col]
                col_sql += f" DEFAULT {default_value}"
            cols_sql.append(col_sql)
        cols_sql.append(
            f"PRIMARY KEY ({', '.join(columns_primary_key)})"
        )

        sql = f"CREATE TABLE IF NOT EXISTS {schema}.{table} "
        sql += f"({', '.join(cols_sql)})"

        self.execute(
            sql=sql,
            db_pool_conn=db_pool_conn,
        )

    def generate_log_data_path(
        self,
        file_path: str,
        database: str,
        mode: str,
        schema: str = None,
        table: str = None,
        owner: str = None,
        transform_func: str = None,
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Generates log of data path when ingest raw data to minIO

        :param file_path: path to raw data file in minIO
        :param database: database platform where the processed data
            will be stored
        :param mode: the storage mode where the raw data is located in minIO
            the value accepted is 'prod' or 'stag'
        :param schema: schema where the processed data will be stored
            defaults to None
        :param table: table where the processed data will be stored
            defaults to None
        :param owner: name of owner belonging to the raw data path
            defaults to None
        :param transform_func: name of the transform function that
            is used to transform the raw data
            defaults to None
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        if mode == 'prod':
            df = pd.DataFrame(
                {
                    'log_date': str(
                        datetime.datetime.now().replace(microsecond=0)
                        + datetime.timedelta(hours=7)
                    ),
                    'db_type': database,
                    'schema': schema,
                    'table_name': table,
                    'file_path': file_path,
                    'status': 0,
                    'owner': owner,
                    'transform_func': transform_func,
                },
                index=[0],
            )

            self.upsert_data(
                data=df,
                schema='metadata',
                table='platform_log_raw_data',
                primary_keys=['log_date', 'file_path'],
                db_pool_conn=db_pool_conn,
            )

            logging.info('Done generating log data path')

    def update_log_data_path(
        self,
        file_path: str,
        log_date: str,
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Update the status of the log of raw data path to success
            to tracking whether the raw data is processed
            and load to the database

        :param file_path: path to raw data file in minIO
        :param log_date: the date that the log was generated
            the date format will be 'yyyy-mm-dd'
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        df = pd.DataFrame(
            {
                'log_date': log_date,
                'file_path': file_path,
                'status': 1,
            },
            index=[0],
        )

        self.update_table(
            data=df,
            schema='metadata',
            table='platform_log_raw_data',
            columns=['status'],
            primary_keys=['log_date', 'file_path'],
            db_pool_conn=db_pool_conn,
        )

        logging.info('Done updating log data path')

    def get_unload_data_path(
        self,
        transform_func: str,
        db_pool_conn: Callable = None,
    ) -> pd.DataFrame:
        """
        Get all the raw data path the is not processed
            and load to the database in the current date
            based on the name of the transform function

        :param transform_func: name of the transform function
            to process the raw data
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used

        :return: a dataframe contains the information
            about the log raw data path
        """

        current_date = str(
            (
                datetime.datetime.now().replace(microsecond=0)
                + datetime.timedelta(hours=7)
            ).date()
        )
        sql = "SELECT * FROM metadata.platform_log_raw_data "
        sql += f"WHERE (CAST(log_date as DATE) = '{current_date}' "
        sql += f"AND transform_func = '{transform_func}' "
        sql += "AND status = 0)"

        df = self.get_data(
            sql=sql,
            db_pool_conn=db_pool_conn,
        )
        df.sort_values(
            by=['log_date'],
            ascending=True,
            inplace=True,
        )

        logging.info(f'Total {len(df)} unload data path in {current_date}')

        return df

    def truncate_table(
        self,
        schema: str,
        table: str,
        reset_identity: bool = False,
        db_pool_conn: Callable = None,
    ) -> None:
        """
        Remove all the data of the table

        :param schema: schema contains table to truncate
        :param table: table name to truncate
        :param reset_identity: whether to reset identity of the table
            defaults to False
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used
        """

        sql = f"TRUNCATE TABLE {schema}.{table}"
        if reset_identity:
            sql += " RESTART IDENTITY"

        self.execute(
            sql=sql,
            db_pool_conn=db_pool_conn,
        )

    def table_exists(
        self,
        schema: str,
        table: str,
        db_pool_conn: Callable = None,
    ) -> bool:
        """
        Check if the table exists in database

        :param schema: schema contains table to check
        :param table: table name to check
        :param db_pool_conn: connection pool contains multiple connections
            to connect to database
            defaults to None
            if None, a new connection will be created and automatically closed
            after being used

        :return: True if table exists and False if not
        """

        sql = "SELECT EXISTS (SELECT FROM pg_tables WHERE "
        sql += f"schemaname = '{schema}' AND tablename  = '{table}')"

        exists = self.get_data(
            sql=sql,
            db_pool_conn=db_pool_conn,
        )['exists'].values[0]

        return exists
