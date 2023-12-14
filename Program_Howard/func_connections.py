'''
This file contains the functions that connect to the DYDX API
'''


from decouple import config
from dydx3 import Client
from web3 import Web3
from constants import (
    HOST,
    ETHERUEM_ADDRESS,
    DYDX_API_KEY,
    DYDX_API_SECRET,
    DYDX_API_PASSPHRASE,
    STARK_PRIVATE_KEY,
    HTTP_PROVIDER,
)

# Connect to DYDX
def connect_to_dydx():
    '''
    Connect to DYDX with the pre-defined keys in constants.py
    return the client status for operations
    '''
    # Create Client
    client = Client(
    host=HOST,
    api_key_credentials={
        "key": DYDX_API_KEY,
        "secret": DYDX_API_SECRET,
        "passphrase": DYDX_API_PASSPHRASE,
    },
    stark_private_key= STARK_PRIVATE_KEY,
    eth_private_key= config("ETH_PRIVATE_KEY"),
    default_ethereum_address= ETHERUEM_ADDRESS,
    web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER))
    )


    # Confirm Client is Connected
    account = client.private.get_account()
    account_id = account.data["account"]["id"]
    quote_balance = account.data["account"]["quoteBalance"]
    print("Connection successful")
    print("Account ID:", account_id)
    print("Quote Balance:", quote_balance)

    # Return Client
    return client
