import re
import inspect
import logging
import warnings
from .y4a_telegram import send_message

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def telegram_alert(context) -> None:
    """
    Airflow DAG failure notification to Telegram
    """

    owner = '@' + context['dag'].default_args['owner']

    message = f"\u26d4 *{context['task_instance']}*\n"
    message += f"Owner: {owner}\n"
    message += f"DAG ID: *{context['task_instance'].dag_id}*\n"
    message += f"Task ID: *{context['task_instance'].task_id}*\n"
    message += f"Execution Time: *{context['task_instance'].execution_date}*\n"
    message += f"Error: *{context['exception']}*\n"
    log_url = str(context['task_instance'].log_url)
    log_url = log_url.replace('localhost', 'af-in-master-sop.yes4all.internal')
    message += f"Log URL: [Link]({log_url})"

    telegram_token = "6318613524:AAG3_JGEsTZbSvcupG5aJk-jZPzghuf3yZ4"
    chat_id = "-868321875"

    send_message(
        text=message,
        bot_token=telegram_token,
        chat_id=chat_id,
    )


def auto_dag_id() -> str:
    """
    Auto naming for the Airflow DAG ID based on the file directory

    :return: name of the Airflow DAG ID
    """

    current_frame = inspect.currentframe()
    current_path = inspect.getfile(current_frame.f_back)
    airflow_path = current_path.split('/airflow/dags/')[-1]
    airflow_path = airflow_path.replace('sop_ingestion', 'de')
    dag_id = airflow_path\
        .replace('.py', '')\
        .lower().strip()
    dag_id = re.sub(
        r'[^a-zA-Z0-9/]+',
        '_',
        dag_id,
    )
    dag_id = dag_id.replace('/', '.')

    return dag_id
