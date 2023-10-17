import logging
import warnings
from psycopg2 import connect
import requests

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def grant_table(
    schema: str,
    table: str,
    list_users: list,
    db_host: str,
    db: str = 'serving',
    privileges: list = ['SELECT'],
    all_privileges: bool = False,
):
    response = requests.get(
        'http://172.30.15.171:5431/v1/users/credentials'
        '/pg/da_admin'
    )

    credentials = response.json()

    hosts = {
        'raw_master': '172.30.12.153',
        'raw_repl': '172.30.12.154',
        'serving_master': '172.30.12.153',
        'serving_repl': '172.30.12.154',
    }

    conn = connect(
        user=credentials['user_name'],
        password=credentials['password'],
        host=hosts[db_host],
        port=5432,
        database=db,
    )

    try:
        cur = conn.cursor()

        for user in list_users:
            if all_privileges:
                sql = f"GRANT ALL PRIVILEGES ON {schema}.{table} to {user}"
            else:
                privileges_sql = ', '.join(privileges)
                sql = f"GRANT {privileges_sql} ON {schema}.{table} to {user}"

            cur.execute(sql)
            logging.info(sql)

        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(e)
        conn.close()
