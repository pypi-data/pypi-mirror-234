import requests


def get_credentials(
    platform: str,
    account_name: str,
) -> None:
    response = requests.get(
        f'http://172.30.15.171:5431/v1/users/credentials'
        f'/{platform}/{account_name}'
    )

    return response.json()
