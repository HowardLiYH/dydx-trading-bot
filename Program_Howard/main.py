'''
The Main Program for the Howard DYDX Trading Bot
'''


from func_connections import connect_to_dydx
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED_PAIRS
from func_private import abort_all_positions
from func_public import construct_market_prices


if __name__ == "__main__":

    # Connect to Client
    try:
        print("Connecting to client...")
        client = connect_to_dydx()
    except Exception as e:
        print(e)
        print("Error connected to client: ", e)
        exit(1)


    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all Positions...")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error closing all positions: ", e)
            exit(1)

    # Find Cointegrated Pairs
    if FIND_COINTEGRATED_PAIRS:

        # Construct Market Prices
        try:
            print("Fetching Market Prices, please allow 3 mins...")
            df_makret_prices = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e)
            exit(1)
