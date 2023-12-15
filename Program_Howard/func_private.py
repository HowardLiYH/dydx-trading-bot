'''
Connecting DYDX Private requests
'''

from datetime import datetime, timedelta
import time
import json
from pprint import pprint
from func_utils import format_number


# Get existing open positions
def is_open_positions(client, market):

    # Protect API
    time.sleep(0.2)

    # Get positions
    all_positions = client.private.get_positions(
        market=market,
        status="OPEN"
    )

    # Determine if open
    if len(all_positions.data['positions']) > 0:
        return True
    else:
        return False



# Check order status
def check_order_status(client, order_id):
    '''
        Input:
            1) Client information from func_connections.py
            2) Order ID
        Output:
            1) Order status
    '''
    order = client.private.get_order_by_id(order_id)
    if order.data:
        if "order" in order.data.keys():
            return order.data['order']['status']
    return "FAILED"





# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
    '''
        Input:
            1) Client information from func_connections.py
            2) Market to place order on, etc. "BTC-USD"
            3) Side of the order, etc. "BUY"
            4) Size of the order, etc. "0.01"
            5) Price of the order, etc. "10000"
            6) Reduce only, etc. True or False
        Output:
            1) Order information
    '''
    print("place_market_order: start")

    # Get Position ID
    account_resposne = client.private.get_account()
    position_id = account_resposne.data['account']['positionId']
    print(f"place_market_order: position_id obtained: {position_id}")

    # Get expiration time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(server_time.data['iso'].replace('Z','+00:00')) + timedelta(seconds=70)


    # Place an order
    placed_order = client.private.create_order(
        position_id= position_id,
        market=market,
        side=side,
        order_type='MARKET',
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK",
        reduce_only=reduce_only
    )

    # Return result
    return placed_order.data




# Abort all open positions
def abort_all_positions(client):
    '''
        Input:
            Client status on DYDX
        Ouput:
            Close all exisisting positions
    '''

    # Cancel all orders
    client.private.cancel_all_orders()

    # Protect API
    time.sleep(0.5)

    # Get markets for reference of tick size
    markets = client.public.get_markets().data

    # pprint(markets)

    # Protect API
    time.sleep(0.5)

    # Get all open positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data['positions']


    # Handle open positions
    close_orders = []
    if len(all_positions) > 0:

        # Leep through each position
        for position in all_positions:

            #Determine Market
            market = position['market']

            # Determine closing side based on existing side
            side = "BUY"
            if position["side"] == 'LONG':
                side = "SELL"


            # Get Price
            price = float(position['entryPrice'])
            # Worst acceptable price
            # For test purpouse, default to 70% of entry price for longs and 30% for shorts
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            # Asjust price to the right decimal
            accept_price = format_number(accept_price, tick_size)

            # Place order to close
            order =  place_market_order(
                client,
                market,
                side,
                position['sumOpen'],
                accept_price,
                True
            )

            # Attempt the reuslt
            close_orders.append(order)

            # Protect API
            time.sleep(0.2)

            # Append the result
            close_orders.append(order)

            # Protect API
            time.sleep(0.2)

    # Override json file with empty list
    bot_agent = []
    with open("bot_agents.json", "w") as outfile:
        json.dump(bot_agent, outfile)

    # Return closed orders
    return close_orders
