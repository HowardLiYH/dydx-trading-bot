'''
The Main Program for the Howard DYDX Trading Bot
'''

import pandas as pd
from func_connections import connect_to_dydx
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED_PAIRS, RESOLUTION, PLACE_TRADES, MANAGE_EXITS
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from func_messaging import send_message




if __name__ == "__main__":

    # Message on start
    send_message("Bot launch successful")

    # Connect to Client
    try:
        print("Connecting to client...")
        client = connect_to_dydx()
    except Exception as e:
        print(e)
        print("Error connected to client: ", e)
        send_message(f"Failed to connect to client {e}")
        exit(1)


    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all Positions...")
            close_orders = abort_all_positions(client)
        except Exception as e:
            print("Error closing all positions: ", e)
            send_message(f"Error closing all positions {e}")
            exit(1)

    # Find Cointegrated Pairs
    if FIND_COINTEGRATED_PAIRS:

        # Construct Market Prices
        try:
            print("Fetching Market Prices, please allow 3 mins...")
            df_makret_prices = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e)
            send_message(f"Error constructing market prices {e}")
            exit(1)

         # Store Cointegrated Pairs
        try:
            print("Storing cointegrated pairs...")
            store_results = store_cointegration_results(df_makret_prices)
            df_csv = pd.read_csv("cointegrated_pairs.csv")
            print(f"Cointegrated pairs CSV produced given {RESOLUTION} window with {len(df_csv)} results!")
            if store_results != "saved":
                print("Error storing cointegrated pairs")
                exit(1)
        except Exception as e:
            print("Error saving cointegrated pairs: ", e)
            send_message(f"Error saving cointegrated pairs {e}")
            exit(1)

    # Run as always on
    while True:
        # Place trades for closing positions
        if MANAGE_EXITS:
            try:
                print("Mnaging exists...")
                manage_trade_exits(client)
            # TypeError with NoneType Occurs when the initial set amount per trade become indivisible for the given size
            # Can be ignored for now, but should be modified accordingly when goes onto exchanges
            except Exception as e:
                print("Error managing exiting positions: ", e)
                send_message(f"Error managing exit positions {e}")
                exit(1)


        # Place trades for opening positions
        if PLACE_TRADES:
            try:
                print("Finding trading opportunities...")
                open_positions(client)
            # TypeError with NoneType Occurs when the initial set amount per trade become indivisible for the given size
            # Can be ignored for now, but should be modified accordingly when goes onto exchanges
            except TypeError as e:
                print("\n")
                print("********")
                print("Error: 'NoneType' object is not subscriptable")
                print("********\n")
            except Exception as e:
                print("Error trading pairs: ", e)
                send_message(f"Error opening trades {e}")
                exit(1)
