import os
import logging
import configparser
import warnings
from typing import Callable
import pandas as pd
import gspread
from gspread.exceptions import APIError
from ..y4a_credentials import get_credentials

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class GGSheetUtils:
    """
    Utils for Google Sheets

    :param account_name: the client account name for Google Sheet
    """

    def __init__(
        self,
        account_name: str,
    ) -> None:
        self.account_name = account_name
        self.credentials = get_credentials(
            platform='gg_api',
            account_name=self.account_name,
        )

        self.email = self.credentials['email']
        self.private_key = self.credentials['secret_key']

        self.auth_dict = {
            'client_email': self.email,
            'private_key': self.private_key,
            'token_uri': 'https://oauth2.googleapis.com/token',
        }

        self.client = gspread.service_account_from_dict(self.auth_dict)

    def open_spread_sheet(
        self,
        sheet_id: str,
    ) -> Callable:
        spread_sheet = self.client.open_by_key(
            key=sheet_id,
        )

        return spread_sheet

    def create_spread_sheet(
        self,
        sheet_name: str,
        folder_id: str,
        share_to: list = [],
    ) -> Callable:
        spread_sheet = self.client.create(
            title=sheet_name,
            folder_id=folder_id,
        )
        if share_to:
            for mail in share_to:
                spread_sheet.share(
                    email_address=mail,
                    perm_type='user',
                    role='writer',
                )

        return spread_sheet
    
    def get_work_sheet(
        self,
        spread_sheet: Callable,
        sheet_name: str,
    ) -> Callable:
        work_sheet = spread_sheet.worksheet(sheet_name)

        return work_sheet
    
    def list_all_work_sheets(
        self,
        spread_sheet: Callable,
    ) -> list:
        work_sheets = spread_sheet.worksheets()

        return work_sheets
    
    def delete_work_sheet(
        self,
        spread_sheet: Callable,
        work_sheet: Callable,
    ) -> None:
        spread_sheet.del_worksheet(work_sheet)

    def clear_work_sheets(
        self,
        work_sheet: Callable,
    ) -> None:
        work_sheet.clear()

    def get_data(
        self,
        sheet_id: str,
        sheet_name: str = None,
        range_from: str = 'A',
        range_to: str = 'Z',
        columns_first_row: bool = False,
    ) -> pd.DataFrame:
        """
        Get data from the given sheet

        :param sheet_id: the id of the sheet
        :param sheet_name: the name of the sheet
            defaults to None
        :param range_from: the begining of the range
            of data from sheet to get
            defaults to A
        :param range_to: the end of the range
            of data from sheet to get
            defaults to Z
        :param columns_first_row: whether to convert the first row
            to columns
            defaults to False

        :return: the dataframe contains data from sheet
        """

        url_content = self.client.open_by_url(
            f'https://docs.google.com/spreadsheets/d/{sheet_id}'
        )

        data_range = f'{range_from}:{range_to}'
        if sheet_name:
            data_range = f'{sheet_name}!{data_range}'

        try:
            data = url_content.values_get(data_range)['values']
            df = pd.DataFrame(data)
            if columns_first_row:
                df.columns = df.iloc[0].to_list()
                df = df.iloc[1:].reset_index(drop=True)
        except APIError as e:
            logging.error(e)
            df = pd.DataFrame()

        return df
