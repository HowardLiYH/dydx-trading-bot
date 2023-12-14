'''
Define functions will be used to calculate cointegration
'''


import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from constants import MAX_HALF_LIFE, WINDOW


# Calculate Half Life
# https://www.pythonforfinance.net/2016/05/09/python-backtesting-mean-reversion-part-2/


def calculate_half_life(spread):
    '''
        Calculate the half life of the spread using OLS
        Return the half life
    '''
    df_spread = pd.DataFrame(spread, columns=["spread"])
    spread_lag = df_spread.shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_ret = pd.DataFrame(df_spread.spread - spread_lag.iloc[:, 0])
    spread_ret.iloc[0] = spread_ret.iloc[1]
    spread_lag2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_ret, spread_lag2)
    res = model.fit()
    half_life = int(round(-np.log(2) / res.params[1], 0))
    return half_life


# Calculate ZScore
def calculate_zscore(spread):
    spread_series = pd.Series(spread)
    mean = spread_series.rolling(window=WINDOW).mean()
    std = spread_series.rolling(window=WINDOW).std()
    x = spread_series.rolling(window=1).mean()
    zscore = (x - mean) / std
    return zscore


# Calculate Cointegration
def calculate_cointegration(series_1, series_2):
    '''
        Calculate the cointegration of two series
        Return the cointegration flag, hedge ratio, and half life
    '''
    series_1 = np.array(series_1).astype(np.float)
    series_2 = np.array(series_2).astype(np.float)
    coint_flag = 0

    # The default coint method here from statsmodel is
    # the Augmented Engled Granger Model
    coint_res = coint(series_1, series_2)

    # The t-statistic of unit-root test on residuals.
    coint_t = coint_res[0]

    # MacKinnon”s approximate, asymptotic p-value based on MacKinnon (1994).
    # If p_value is less than 0.05, it is cointegrated
    p_value = coint_res[1]

    # Critical values for the test statistic at the 1 %, 5 %, and 10 % levels
    # based on regression curve. This depends on the number of observations.
    critical_value = coint_res[2][1]
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = series_1 - (hedge_ratio * series_2)
    half_life = calculate_half_life(spread)

    # Check on channle for extensive conversation on t_check
    # the t_value should be less than the critical value
    t_check = coint_t < critical_value
    coint_flag = 1 if p_value < 0.05 and t_check else 0
    return coint_flag, hedge_ratio, half_life


# Store Cointegration Results
def store_cointegration_results(df_market_prices):

    # Initialize
    markets = df_market_prices.columns.tolist()
    criteria_met_paris = []

    print("Finding Cointegrated Pairs...")
    # Find cointegrated pairs
    # Start with our base pair and Loop through each market
    # No reptition will happen here
    for index, base_market in enumerate(markets[:-1]):
        # print(f"Checking {base_market}...")
        series_1 = df_market_prices[base_market].values.astype(float).tolist()

        # Get Quote Pair
        for quote_market in markets[index +1:]:
            # print(f"Checking {quote_market}...")
            series_2 = df_market_prices[quote_market].values.astype(float).tolist()

            # Check Cointegration
            coint_flag, hedge_ratio, half_life = calculate_cointegration(series_1, series_2)
            # print(f"Cointegration: {coint_flag}, Half Life: {half_life}")

            # Log Pair if Cointegrated
            if coint_flag == 1 and half_life <= MAX_HALF_LIFE and half_life > 0:
                criteria_met_paris.append({
                    "base_market": base_market,
                    "quote_market": quote_market,
                    "hedge_ratio": hedge_ratio,
                    "half_life": half_life
                })


    # Create and save DataFrame
    print("Saving Cointegrated Pairs...")
    df_criteria_met = pd.DataFrame(criteria_met_paris)
    df_criteria_met.to_csv("cointegrated_pairs.csv")
    del df_criteria_met

    # Return result
    print("Cointegrated Pairs Successfully Saved")
    return "saved"
