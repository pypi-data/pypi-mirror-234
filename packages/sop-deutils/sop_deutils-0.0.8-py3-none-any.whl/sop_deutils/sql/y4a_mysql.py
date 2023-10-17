import logging
import datetime
import warnings
import mysql.connector
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class MySQLUtils:
    def __init__(
        self,
        db_user: str,
        db_password: str,
        db_host: str,
    ) -> None:
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host

    def _serialize_cell(
        self,
        cell,
    ):
        if cell is None:
            return None
        if isinstance(cell, datetime.datetime):
            return cell.isoformat()

        return str(cell)

    def connect(
        self,
        database: str,
    ):
        conn = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=database,
        )

        return conn

    def read_sql_file(
        self,
        sql_file_path: str,
    ):
        with open(sql_file_path, 'r') as file:
            sql = file.read()

        return sql

    def insert_data(
        self,
        data: pd.DataFrame,
        database: str,
        table: str,
        replace: bool = False,
        commit_every: int = 1000,
    ):
        if len(data) == 0:
            return

        conn = self.connect(database)
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
            if not replace:
                sql = "INSERT INTO "
            else:
                sql = "REPLACE INTO "
            sql += "{0} {1} VALUES ({2})".format(
                table,
                target_fields,
                ",".join(placeholders)
            )
            cur.execute(sql, values)
            if i % commit_every == 0:
                conn.commit()
                logging.info(
                    f"Loaded {i} into {table} rows so far"
                )

        conn.commit()
        conn.close()

        logging.info(
            f"Done loading. Loaded a total of {i} rows"
        )

    def update_table(
        self,
        data: pd.DataFrame,
        database: str,
        table: str,
        columns: list,
        primary_keys: list,
        commit_every: int = 1000,
    ):
        if len(data) == 0:
            return

        conn = self.connect(database)
        cur = conn.cursor()

        sql = f"UPDATE {table} SET "
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
                lst.append(self._serialize_cell(cell))
            values = tuple(lst)
            cur.execute(sql, values)
            if i % commit_every == 0:
                conn.commit()
                logging.info(
                    f"Updated {i} to {table} rows so far"
                )

        conn.commit()
        conn.close()

        logging.info(
            f"Done updating. Updated a total of {i} rows"
        )

    def get_data(
        self,
        sql: str,
        database: str,
    ):
        conn = self.connect(database)

        data = pd.read_sql(
            sql=sql,
            con=conn,
        )

        conn.close()

        return data

    def select_distinct(
        self,
        col: str,
        database: str,
        table: str,
    ):
        conn = self.connect(database)
        sql = f"SELECT DISTINCT {col} "
        sql += f"FROM {table}"

        data = pd.read_sql(
            sql=sql,
            con=conn,
        )[col].to_list()

        conn.close()

        return data

    def show_columns(
        self,
        database: str,
        table: str,
    ):
        columns = self.get_data(
            sql=f"SHOW COLUMNS FROM {table}",
            database=database,
        )['Field'].to_list()

        return columns

    def add_column(
        self,
        database: str,
        table: str,
        column_name: str,
        dtype: str,
    ):
        sql = f"ALTER TABLE {table} "
        sql += f"ADD COLUMN {column_name} {dtype}"

        self.execute(
            sql=sql,
            database=database,
        )

    def execute(
        self,
        sql: str,
        database: str,
    ):
        conn = self.connect(database)
        cur = conn.cursor()

        cur.execute(sql)

        conn.commit()

        cur.close()
        conn.close()
