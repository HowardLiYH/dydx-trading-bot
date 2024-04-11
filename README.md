![image](https://github.com/HowardLiYH/dydx-trading-bot/assets/60827239/ab62edcf-6fd5-47c2-9582-c21819639e81)


# Automated Pair Trading on DYDX (V3)

![Screenshot 2023-12-11 at 1 52 27 AM](https://github.com/HowardLiYH/dydx-trading-bot/assets/60827239/22a1623b-2d25-4a80-a7a0-e57845573f79)

### Development Stage on Sepolia, ETH Testnet:

[Stage 1] ✅
- Set up connections to DYDX
- Place Market Order
- Abort All Orders

[Stage 2]  ✅
- Construct Cointegrated Pairs
- Store Cointegrated Pairs
- Create Entry Conditions
- Create Exit Conditions

[Stage 3]  ✅
- Manage Existing Trades
- Open Positions
- Test Operation

[Deployment] ✅
- Telegram Messaging 
- AWS Cloud Deployment
- To receive Bot Updates and view current status, please go to Telegram and visit [@howard_dydx_bot](https://t.me/howard_dydx_bot)

[Usage Improvements] 
- Consider migrating onto exchanges for better liquidity and stable developing environments
- Adjust formula and constants to calculate more rigorous hedge ratio, half-life, and other parameters
- Adjust capital allocation rules following the Kelly Criterion
- Adjust exit rules
- Build a UI (React, FastAPI, Telegram)
- Add ML for position sizing (eg. XGBoost to define the confidence of the model given specific trades for determining the amount of capital that should be used)





