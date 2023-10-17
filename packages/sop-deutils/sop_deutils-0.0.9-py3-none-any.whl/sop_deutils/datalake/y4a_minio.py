import logging
import warnings
from io import BytesIO
from minio import Minio
import pandas as pd
from ..y4a_credentials import get_credentials

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class MinioUtils:
    """
    Utils for MinIO storage

    :param account_name: the client account name to minio storage
    """
    def __init__(
        self,
        account_name: str,
    ) -> None:
        self.account_name = account_name
        self.credentials = get_credentials(
            platform='minio',
            account_name=self.account_name,
        )
        self.access_key = self.credentials['access_key']
        self.secret_key = self.credentials['secret_key']

        self.client = Minio(
            endpoint='storage-api.yes4all.internal',
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )

    def data_exist(
        self,
        mode: str,
        file_path: str,
        bucket_name: str = 'sc-bucket',
    ) -> bool:
        """
        Check if the data file exists in a directory

        :param mode: the data storage mode
            the value is either 'prod' or 'stag'
        :param file_path: the directory to check
            notes that the path is considered after
            the data storage mode parent directory
            and remove the ".parquet" extension
        :param bucket_name: the name of the bucket to check
            defaults to 'sc-bucket'

        :return: True if the data file exists
            otherwise False
        """

        obj = self.client.list_objects(
            bucket_name=bucket_name,
            prefix=f'{mode}{file_path}.parquet'
        )
        obj = [*obj]

        if len(obj) == 0:
            return False
        return True

    def get_data_value_exist(
        self,
        mode: str,
        file_path: str,
        column_key: str,
        bucket_name: str = 'sc-bucket',
    ) -> list:
        """
        Get the distinct values of a specified column
            of data in the data directory

        :param mode: the data storage mode
            the value is either 'prod' or 'stag'
        :param file_path: the directory to get distinct values
            notes that the path is considered after
            the data storage mode parent directory
            and remove the ".parquet" extension
        :param column_key: the column name to get distinct values
        :param bucket_name: the name of the bucket
            to get distinct values
            defaults to 'sc-bucket'

        :return: list of distinct values
        """

        df = self.get_data_wildcard(
            mode,
            file_path,
            bucket_name,
        )

        if len(df) == 0:
            return list()

        return list(df[column_key].unique())

    def load_data(
        self,
        data: pd.DataFrame,
        mode: str,
        file_path: str,
        bucket_name: str = 'sc-bucket',
    ) -> None:
        """
        Load data from dataframe to storage

        :param data: dataframe contains data to load
        :param mode: the data storage mode
            the value is either 'prod' or 'stag'
        :param file_path: the directory to load the data
            notes that the path is considered after
            the data storage mode parent directory
            and remove the ".parquet" extension
        :param bucket_name: the name of the bucket
            to load the data
            defaults to 'sc-bucket'
        """

        if mode not in ['prod', 'stag']:
            logging.error('Mode must be prod or stag')
            return

        parquet_data = data.to_parquet(index=False)
        bytes_data = BytesIO(parquet_data)

        self.client.put_object(
            bucket_name=bucket_name,
            object_name=f'{mode}{file_path}.parquet',
            data=bytes_data,
            length=bytes_data.getbuffer().nbytes,
            content_type=f'{mode}/parquet',
        )

        logging.info('Done loading data to Minio storage')

    def get_data(
        self,
        mode: str,
        file_path: str,
        bucket_name: str = 'sc-bucket',
    ) -> pd.DataFrame:
        """
        Get data from a single file of directory of storage

        :param mode: the data storage mode
            the value is either 'prod' or 'stag'
        :param file_path: the directory to get the data
            notes that the path is considered after
            the data storage mode parent directory
            and remove the ".parquet" extension
        :param bucket_name: the name of the bucket
            to get the data
            defaults to 'sc-bucket'

        :return: dataframe contains data to get
        """

        if mode not in ['prod', 'stag']:
            logging.error('Mode must be prod or stag')
            return

        parquet_data = BytesIO(
            self.client.get_object(
                bucket_name=bucket_name,
                object_name=f'{mode}{file_path}.parquet',
            ).data
        )
        df = pd.read_parquet(parquet_data)

        return df

    def get_data_wildcard(
        self,
        mode: str,
        file_path: str,
        bucket_name: str = 'sc-bucket',
    ) -> pd.DataFrame:
        """
        Get data from multiple files of directories of storage

        :param mode: the data storage mode
            the value is either 'prod' or 'stag'
        :param file_path: the parent directory to get the data
            notes that the path is considered after
            the data storage mode parent directory
        :param bucket_name: the name of the bucket
            to get the data
            defaults to 'sc-bucket'

        :return: dataframe contains data to get
        """

        data = list()

        if mode not in ['prod', 'stag']:
            logging.error('Mode must be prod or stag')
            return

        objects = self.client.list_objects(
            bucket_name=bucket_name,
            prefix=f'{mode}{file_path}',
            recursive=True,
        )

        num_objects = 0
        for obj in objects:
            if '.parquet' in obj.object_name:
                file_name = obj.object_name.replace(
                    '.parquet', ''
                ).replace(
                    f'{mode}/', '/'
                )
                data.append(
                    self.get_data(
                        mode,
                        file_name,
                        bucket_name,
                    )
                )
                num_objects += 1
                if num_objects % 100 == 0:
                    logging.info(f'Got {num_objects} objects')

        if len(data) > 0:
            df = pd.concat(data).reset_index(drop=True)
            return df

        return pd.DataFrame()
