import pandas as pd
import json
import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np

# Glassnode API key
API_KEY = '...'

# ETH
# ---Create time range for final table
start_date = datetime.date(2015, 8, 1)
end_date = datetime.date.today()
num_days = (end_date - start_date).days
dates = [start_date]
for i in range(num_days):
    next_day = dates[-1] + datetime.timedelta(days=1)
    dates.append(next_day)

# ---Create base dataframe that will be used to create individual site locations dataframes
base_df = pd.DataFrame()
base_df['Dates'] = dates
base_df.set_index(base_df['Dates'], inplace=True)
base_df.drop('Dates', 1, inplace=True)

# ---Main Table
ETH = base_df

# ---DeFi
defi_TVL_res = requests.get('https://api.glassnode.com/v1/metrics/defi/total_value_locked',
                            params={'a': 'ETH', 'api_key': API_KEY})

try:
    defi_TVL = pd.read_json(defi_TVL_res.text, convert_dates=['t'])
    defi_TVL.rename(columns={'t': 'Date', 'v': 'ETH Total Value Locked'}, inplace=True)
    defi_TVL.set_index('Date', inplace=True)
    ETH['ETH Total Value Locked'] = defi_TVL
except (ValueError, NameError):
    print('ETH Total Value Locked - Error')

# ---ETH 2.0
total_value_staked_res = requests.get('https://api.glassnode.com/v1/metrics/eth2/staking_total_volume_sum',
                                      params={'a': 'ETH', 'api_key': API_KEY})
total_number_of_validators_res = requests.get(
    'https://api.glassnode.com/v1/metrics/eth2/staking_total_validators_count', params={'a': 'ETH', 'api_key': API_KEY})

try:
    total_value_staked = pd.read_json(total_value_staked_res.text, convert_dates=['t'])
    total_value_staked.rename(columns={'t': 'Date', 'v': 'ETH Total Value Staked'}, inplace=True)
    total_value_staked.set_index('Date', inplace=True)
    ETH['ETH Total Value Staked'] = total_value_staked
except (ValueError, NameError):
    print('ETH Total Value Staked - Error')
try:
    total_number_of_validators = pd.read_json(total_number_of_validators_res.text, convert_dates=['t'])
    total_number_of_validators.rename(columns={'t': 'Date', 'v': 'ETH Total Number of Validators'}, inplace=True)
    total_number_of_validators.set_index('Date', inplace=True)
    ETH['ETH Total Number of Validators'] = total_number_of_validators
except (ValueError, NameError):
    print('ETH Total Number of Validators - Error')

# ---Fees
gas_used_total_res = requests.get('https://api.glassnode.com/v1/metrics/fees/gas_used_sum',
                                  params={'a': 'ETH', 'api_key': API_KEY})
gas_used_mean_res = requests.get('https://api.glassnode.com/v1/metrics/fees/gas_used_mean',
                                 params={'a': 'ETH', 'api_key': API_KEY})
gas_pric_mean_res = requests.get('https://api.glassnode.com/v1/metrics/fees/gas_price_mean',
                                 params={'a': 'ETH', 'api_key': API_KEY})

try:
    gas_used_total = pd.read_json(gas_used_total_res.text, convert_dates=['t'])
    gas_used_total.rename(columns={'t': 'Date', 'v': 'ETH Total Gas Used'}, inplace=True)
    gas_used_total.set_index('Date', inplace=True)
    ETH['ETH Total Gas Used'] = gas_used_total
except (ValueError, NameError):
    print('ETH Total Gas Used - Error')
try:
    gas_used_mean = pd.read_json(gas_used_mean_res.text, convert_dates=['t'])
    gas_used_mean.rename(columns={'t': 'Date', 'v': 'ETH Mean Gas Used'}, inplace=True)
    gas_used_mean.set_index('Date', inplace=True)
    ETH['ETH Mean Gas Used'] = gas_used_mean
except (ValueError, NameError):
    print('ETH Mean Gas Used - Error')
try:
    gas_pric_mean = pd.read_json(gas_pric_mean_res.text, convert_dates=['t'])
    gas_pric_mean.rename(columns={'t': 'Date', 'v': 'ETH Mean Gas Price'}, inplace=True)
    gas_pric_mean.set_index('Date', inplace=True)
    ETH['ETH Mean Gas Price'] = gas_pric_mean
except (ValueError, NameError):
    print('ETH Mean Gas Price - Error')

# ---Indicators
NVT_signal_res = requests.get('https://api.glassnode.com/v1/metrics/indicators/nvts',
                              params={'a': 'ETH', 'api_key': API_KEY})
NUPL_res = requests.get('https://api.glassnode.com/v1/metrics/indicators/net_unrealized_profit_loss',
                        params={'a': 'ETH', 'api_key': API_KEY})

try:
    NVT_signal = pd.read_json(NVT_signal_res.text, convert_dates=['t'])
    NVT_signal.rename(columns={'t': 'Date', 'v': 'ETH NVT Signal'}, inplace=True)
    NVT_signal.set_index('Date', inplace=True)
    ETH['ETH NVT Signal'] = NVT_signal
except (ValueError, NameError):
    print('ETH NVT Signal - Error')
try:
    NUPL = pd.read_json(NUPL_res.text, convert_dates=['t'])
    NUPL.rename(columns={'t': 'Date', 'v': 'ETH NUPL'}, inplace=True)
    NUPL.set_index('Date', inplace=True)
    ETH['ETH NUPL'] = NUPL
except (ValueError, NameError):
    print('ETH NUPL - Error')

# ---Market
price_res = requests.get('https://api.glassnode.com/v1/metrics/market/price_usd_close',
                         params={'a': 'ETH', 'api_key': API_KEY})
OHLC_res = requests.get('https://api.glassnode.com/v1/metrics/market/price_usd_ohlc',
                        params={'a': 'ETH', 'api_key': API_KEY})
market_cap_res = requests.get('https://api.glassnode.com/v1/metrics/market/marketcap_usd',
                              params={'a': 'ETH', 'api_key': API_KEY})
realized_cap_res = requests.get('https://api.glassnode.com/v1/metrics/market/marketcap_realized_usd',
                                params={'a': 'ETH', 'api_key': API_KEY})
realized_price_res = requests.get('https://api.glassnode.com/v1/metrics/market/price_realized_usd',
                                  params={'a': 'ETH', 'api_key': API_KEY})

try:
    price = pd.read_json(price_res.text, convert_dates=['t'])
    price.rename(columns={'t': 'Date', 'v': 'ETH Price'}, inplace=True)
    price.set_index('Date', inplace=True)
    ETH['ETH Price'] = price
except (ValueError, NameError):
    print('ETH Price - Error')
try:
    OHLC = pd.read_json(OHLC_res.text, convert_dates=['t'])
    OHLC.rename(columns={'t': 'Date', 'v': 'ETH OHLC'}, inplace=True)
    OHLC.set_index('Date', inplace=True)
    ETH['ETH OHLC'] = OHLC
except (ValueError, NameError):
    print('ETH OHLC - Error')
try:
    market_cap = pd.read_json(market_cap_res.text, convert_dates=['t'])
    market_cap.rename(columns={'t': 'Date', 'v': 'ETH Market Cap'}, inplace=True)
    market_cap.set_index('Date', inplace=True)
    ETH['ETH Market Cap'] = market_cap
except (ValueError, NameError):
    print('ETH Market Cap - Error')
try:
    realized_caps = pd.read_json(realized_cap_res.text, convert_dates=['t'])
    realized_caps.rename(columns={'t': 'Date', 'v': 'ETH Realized Caps'}, inplace=True)
    realized_caps.set_index('Date', inplace=True)
    ETH['ETH Realized Caps'] = realized_caps
except (ValueError, NameError):
    print('ETH Realized Caps - Error')
try:
    realized_price = pd.read_json(realized_price_res.text, convert_dates=['t'])
    realized_price.rename(columns={'t': 'Date', 'v': 'ETH Realized Price'}, inplace=True)
    realized_price.set_index('Date', inplace=True)
    ETH['ETH Realized Price'] = realized_price
except (ValueError, NameError):
    print('ETH Realized Price - Error')

# ---Supply
Supply_in_Profit_res = requests.get('https://api.glassnode.com/v1/metrics/supply/profit_sum',
                                    params={'a': 'ETH', 'api_key': API_KEY})
Supply_in_Loss_res = requests.get('https://api.glassnode.com/v1/metrics/supply/loss_sum',
                                  params={'a': 'ETH', 'api_key': API_KEY})

try:
    Supply_in_Profit = pd.read_json(Supply_in_Profit_res.text, convert_dates=['t'])
    Supply_in_Profit.rename(columns={'t': 'Date', 'v': 'ETH Supply_in_Profit'}, inplace=True)
    Supply_in_Profit.set_index('Date', inplace=True)
    ETH['ETH Supply_in_Profit'] = Supply_in_Profit
except (ValueError, NameError):
    print('ETH Supply_in_Profit - Error')
try:
    Supply_in_Loss = pd.read_json(Supply_in_Loss_res.text, convert_dates=['t'])
    Supply_in_Loss.rename(columns={'t': 'Date', 'v': 'ETH Supply_in_Loss'}, inplace=True)
    Supply_in_Loss.set_index('Date', inplace=True)
    ETH['ETH Supply_in_Loss'] = Supply_in_Loss
except (ValueError, NameError):
    print('ETH Supply_in_Loss - Error')

# ---Transactions
transaction_count_res = requests.get('https://api.glassnode.com/v1/metrics/transactions/count',
                                     params={'a': 'ETH', 'api_key': API_KEY})
transaction_rate_res = requests.get('https://api.glassnode.com/v1/metrics/transactions/rate',
                                    params={'a': 'ETH', 'api_key': API_KEY})

try:
    transaction_count = pd.read_json(transaction_count_res.text, convert_dates=['t'])
    transaction_count.rename(columns={'t': 'Date', 'v': 'ETH Transaction Count'}, inplace=True)
    transaction_count.set_index('Date', inplace=True)
    ETH['ETH Transaction Count'] = transaction_count
except (ValueError, NameError):
    print('ETH Transaction Count - Error')
try:
    transaction_rate = pd.read_json(transaction_rate_res.text, convert_dates=['t'])
    transaction_rate.rename(columns={'t': 'Date', 'v': 'ETH Transaction Rate'}, inplace=True)
    transaction_rate.set_index('Date', inplace=True)
    ETH['ETH Transaction Rate'] = transaction_rate
except (ValueError, NameError):
    print('ETH Transaction Rate - Error')

# BTC
# ---Create time range for final table
start_date = datetime.date(2009, 1, 1)
end_date = datetime.date.today()
num_days = (end_date - start_date).days
dates = [start_date]
for i in range(num_days):
    next_day = dates[-1] + datetime.timedelta(days=1)
    dates.append(next_day)

# ---Create base dataframe that will be used to create individual site locations dataframes
base_df = pd.DataFrame()
base_df['Dates'] = dates
base_df.set_index(base_df['Dates'], inplace=True)
base_df.drop('Dates', 1, inplace=True)

# ---Main Table
BTC = base_df

# ---Distribution
exchange_balance_total_res = requests.get('https://api.glassnode.com/v1/metrics/distribution/balance_exchanges',
                                          params={'a': 'BTC', 'api_key': API_KEY})

try:
    exchange_balance_total = pd.read_json(exchange_balance_total_res.text, convert_dates=['t'])
    exchange_balance_total.rename(columns={'t': 'Date', 'v': 'BTC Total Exchange Balance'}, inplace=True)
    exchange_balance_total.set_index('Date', inplace=True)
    BTC['BTC Total Exchange Balance'] = exchange_balance_total
except (ValueError, NameError):
    print('BTC Total Exchange Balance - Error')

# ---Indicators
RHODL_res = requests.get('https://api.glassnode.com/v1/metrics/indicators/rhodl_ratio',
                         params={'a': 'BTC', 'api_key': API_KEY})
CVDD_res = requests.get('https://api.glassnode.com/v1/metrics/indicators/cvdd', params={'a': 'BTC', 'api_key': API_KEY})
STH_SOPR_res = requests.get('https://api.glassnode.com/v1/metrics/indicators/sopr_less_155',
                            params={'a': 'BTC', 'api_key': API_KEY})
CYD_res = requests.get('https://api.glassnode.com/v1/metrics/indicators/cyd', params={'a': 'BTC', 'api_key': API_KEY})
S2F_res = requests.get('https://api.glassnode.com/v1/metrics/indicators/stock_to_flow_ratio',
                       params={'a': 'BTC', 'api_key': API_KEY})
S2F_deflection_res = requests.get('https://api.glassnode.com/v1/metrics/indicators/stock_to_flow_deflection',
                                  params={'a': 'BTC', 'api_key': API_KEY})

try:
    RHODL = pd.read_json(RHODL_res.text, convert_dates=['t'])
    RHODL.rename(columns={'t': 'Date', 'v': 'BTC RHODL'}, inplace=True)
    RHODL.set_index('Date', inplace=True)
    BTC['BTC RHODL'] = RHODL
except (ValueError, NameError):
    print('BTC RHODL - Error')
try:
    CVDD = pd.read_json(CVDD_res.text, convert_dates=['t'])
    CVDD.rename(columns={'t': 'Date', 'v': 'BTC CVDD'}, inplace=True)
    CVDD.set_index('Date', inplace=True)
    BTC['BTC CVDD'] = CVDD
except (ValueError, NameError):
    print('BTC CVDD - Error')
try:
    STH_SOPR = pd.read_json(STH_SOPR_res.text, convert_dates=['t'])
    STH_SOPR.rename(columns={'t': 'Date', 'v': 'BTC STH_SOPR'}, inplace=True)
    STH_SOPR.set_index('Date', inplace=True)
    BTC['BTC STH_SOPR'] = STH_SOPR
except (ValueError, NameError):
    print('BTC STH_SOPR - Error')
try:
    CYD = pd.read_json(CYD_res.text, convert_dates=['t'])
    CYD.rename(columns={'t': 'Date', 'v': 'BTC CYD'}, inplace=True)
    CYD.set_index('Date', inplace=True)
    BTC['BTC CYD'] = CYD
except (ValueError, NameError):
    print('BTC CYD - Error')
try:
    S2F = pd.read_json(S2F_res.text, convert_dates=['t'])
    S2F.rename(columns={'t': 'Date', 'v': 'BTC S2F'}, inplace=True)
    S2F.set_index('Date', inplace=True)
    BTC['BTC S2F'] = S2F
except (ValueError, NameError):
    print('BTC S2F - Error')
try:
    S2F_deflection = pd.read_json(S2F_deflection_res.text, convert_dates=['t'])
    S2F_deflection.rename(columns={'t': 'Date', 'v': 'BTC S2F Deflection'}, inplace=True)
    S2F_deflection.set_index('Date', inplace=True)
    BTC['BTC S2F Deflection'] = S2F_deflection
except (ValueError, NameError):
    print('BTC S2F Deflection - Error')

# ---Market
price_res = requests.get('https://api.glassnode.com/v1/metrics/market/price_usd_close',
                         params={'a': 'BTC', 'api_key': API_KEY})
OHLC_res = requests.get('https://api.glassnode.com/v1/metrics/market/price_usd_ohlc',
                        params={'a': 'BTC', 'api_key': API_KEY})
market_cap_res = requests.get('https://api.glassnode.com/v1/metrics/market/marketcap_usd',
                              params={'a': 'BTC', 'api_key': API_KEY})
realized_cap_res = requests.get('https://api.glassnode.com/v1/metrics/market/marketcap_realized_usd',
                                params={'a': 'BTC', 'api_key': API_KEY})
realized_price_res = requests.get('https://api.glassnode.com/v1/metrics/market/price_realized_usd',
                                  params={'a': 'BTC', 'api_key': API_KEY})

try:
    price = pd.read_json(price_res.text, convert_dates=['t'])
    price.rename(columns={'t': 'Date', 'v': 'BTC Price'}, inplace=True)
    price.set_index('Date', inplace=True)
    BTC['BTC Price'] = price
except (ValueError, NameError):
    print('BTC Price - Error')
try:
    OHLC = pd.read_json(OHLC_res.text, convert_dates=['t'])
    OHLC.rename(columns={'t': 'Date', 'v': 'BTC OHLC'}, inplace=True)
    OHLC.set_index('Date', inplace=True)
    BTC['BTC OHLC'] = OHLC
except (ValueError, NameError):
    print('BTC OHLC - Error')
try:
    market_cap = pd.read_json(market_cap_res.text, convert_dates=['t'])
    market_cap.rename(columns={'t': 'Date', 'v': 'BTC Market Cap'}, inplace=True)
    market_cap.set_index('Date', inplace=True)
    BTC['BTC Market Cap'] = market_cap
except (ValueError, NameError):
    print('BTC Market Cap - Error')
try:
    realized_caps = pd.read_json(realized_cap_res.text, convert_dates=['t'])
    realized_caps.rename(columns={'t': 'Date', 'v': 'BTC Realized Cap'}, inplace=True)
    realized_caps.set_index('Date', inplace=True)
    BTC['BTC Realized Cap'] = realized_caps
except (ValueError, NameError):
    print('BTC Realized Cap - Error')
try:
    realized_price = pd.read_json(realized_price_res.text, convert_dates=['t'])
    realized_price.rename(columns={'t': 'Date', 'v': 'BTC Realized Price'}, inplace=True)
    realized_price.set_index('Date', inplace=True)
    BTC['BTC Realized Price'] = realized_price
except (ValueError, NameError):
    print('BTC Realized Price - Error')

# ---Mining
thermocap_res = requests.get('https://api.glassnode.com/v1/metrics/mining/thermocap',
                             params={'a': 'BTC', 'api_key': API_KEY})

try:
    thermocap = pd.read_json(thermocap_res.text, convert_dates=['t'])
    thermocap.rename(columns={'t': 'Date', 'v': 'BTC Thermocap'}, inplace=True)
    thermocap.set_index('Date', inplace=True)
    BTC['BTC Thermocap'] = thermocap
except (ValueError, NameError):
    print('BTC Thermocap - Error')

# ---Supply
Supply_in_Profit_res = requests.get('https://api.glassnode.com/v1/metrics/supply/profit_sum',
                                    params={'a': 'BTC', 'api_key': API_KEY})
Supply_in_Loss_res = requests.get('https://api.glassnode.com/v1/metrics/supply/loss_sum',
                                  params={'a': 'BTC', 'api_key': API_KEY})

try:
    Supply_in_Profit = pd.read_json(Supply_in_Profit_res.text, convert_dates=['t'])
    Supply_in_Profit.rename(columns={'t': 'Date', 'v': 'BTC Supply_in_Profit'}, inplace=True)
    Supply_in_Profit.set_index('Date', inplace=True)
    BTC['BTC Supply_in_Profit'] = Supply_in_Profit
except (ValueError, NameError):
    print('BTC Supply_in_Profit - Error')
try:
    Supply_in_Loss = pd.read_json(Supply_in_Loss_res.text, convert_dates=['t'])
    Supply_in_Loss.rename(columns={'t': 'Date', 'v': 'BTC Supply_in_Loss'}, inplace=True)
    Supply_in_Loss.set_index('Date', inplace=True)
    BTC['BTC Supply_in_Loss'] = Supply_in_Loss
except (ValueError, NameError):
    print('BTC Supply_in_Loss - Error')

# ---Self calculated
try:
    BTC['BTC Investor Cap'] = BTC['BTC Realized Cap'] - BTC['BTC Thermocap']
except (ValueError, NameError):
    print('BTC Investor Cap - Error')
try:
    BTC['RPV'] = BTC['BTC NRPL'] / BTC['BTC Realized Cap']
except (ValueError, NameError):
    print('BTC RPV - Error')
try:
    BTC['MVRV'] = BTC['BTC Market Cap'] / BTC['BTC Realized Cap']
except (ValueError, NameError):
    print('BTC MVRV - Error')
try:
    BTC['MVRV_Z_Score'] = (BTC['BTC Market Cap'] - BTC['BTC Realized Cap']) / np.std(BTC['BTC Market Cap'])
except (ValueError, NameError):
    print('BTC MVRV_Z_Score - Error')
try:
    BTC['MVTV'] = BTC['BTC Market Cap'] / BTC['BTC Thermocap']
except (ValueError, NameError):
    print('BTC MVTV - Error')

writer = pd.ExcelWriter(r'C:\Users\amind\Juptyer lab Projects\Crypto Project\Glassnode Data.xlsx')
BTC.to_excel(writer, 'BTC')
ETH.to_excel(writer,'ETH')
writer.save()

BTC = pd.read_excel(r'C:\Users\amind\Juptyer lab Projects\Crypto Project\Glassnode Data.xlsx', sheet_name='BTC')
ETH = pd.read_excel(r'C:\Users\amind\Juptyer lab Projects\Crypto Project\Glassnode Data.xlsx', sheet_name='ETH')
BTC.set_index('Dates', drop=True, inplace=True)
ETH.set_index('Dates', drop=True, inplace=True)

Recent_BTC = BTC.loc[BTC.index >= '2021-01-01']
Recent_ETH = ETH.loc[ETH.index >= '2021-01-01']

#Market Dominance
Total_Crypto_Market_Cap = 2600000000000 #input("Enter Total Cryptocurrency Market Cap:")

BTC_last_valid = BTC['BTC Market Cap'].last_valid_index()
current_BTC_Market_Cap = BTC.loc[BTC_last_valid,'BTC Market Cap']
BTC_dominance = (current_BTC_Market_Cap/float(Total_Crypto_Market_Cap))*100

ETH_last_valid = ETH['ETH Market Cap'].last_valid_index()
current_ETH_Market_Cap = ETH.loc[ETH_last_valid,'ETH Market Cap']
ETH_dominance = (current_ETH_Market_Cap/float(Total_Crypto_Market_Cap))*100

Alt_dominance = 100 - BTC_dominance - ETH_dominance

market_dominance = {'BTC Dominance':  [BTC_dominance],'ETH Dominance': [ETH_dominance],'Alt Dominance': [Alt_dominance]}
writer = pd.ExcelWriter(r'C:\Users\amind\Juptyer lab Projects\Crypto Project\Glassnode Data.xlsx')
market_dominance.to_excel(writer, 'Market Dominance')
writer.save()

#RSI > 30, it is an indication of a bullish trade signal. If it drops below 70, it’s a bearish signal.
BTC_OHLC = Recent_BTC['BTC OHLC'].str.split(n=- 1, expand=True)
BTC_OHLC.rename(columns={1:'BTC Price Close', 3:'BTC Price High', 5:'BTC Price Low', 7:'BTC Price Open'}, inplace=True)
BTC_OHLC.drop([0,2,4,6], axis=1, inplace=True)
BTC_OHLC['BTC Price Close'] = BTC_OHLC['BTC Price Close'].apply(lambda x: float(str(x).replace(',',  '')))
BTC_OHLC['BTC Price High'] = BTC_OHLC['BTC Price High'].apply(lambda x: float(str(x).replace(',',  '')))
BTC_OHLC['BTC Price Low'] = BTC_OHLC['BTC Price Low'].apply(lambda x: float(str(x).replace(',',  '')))
BTC_OHLC['BTC Price Open'] = BTC_OHLC['BTC Price Open'].apply(lambda x: float(str(x).replace('}',  '')))
BTC_delta = BTC_OHLC['BTC Price Close'].diff(1)
BTC_delta.dropna(inplace=True)
BTC_gain = BTC_delta.copy()
BTC_loss = BTC_delta.copy()
BTC_gain[BTC_gain < 0] = 0
BTC_loss[BTC_loss > 0] = 0
time_period = 14
avg_BTC_gain = BTC_gain.rolling(window=time_period).mean()
avg_BTC_loss = abs(BTC_loss.rolling(window=time_period).mean())
BTC_RSI = 100.0 - (100.0 / (1 + (avg_BTC_gain / avg_BTC_loss)))
BTC.drop('BTC OHLC', axis=1, inplace=True)
BTC = BTC.append(BTC_OHLC)
BTC['BTC RSI'] = BTC_RSI

ETH_OHLC = Recent_ETH['ETH OHLC'].str.split(n=- 1, expand=True)
ETH_OHLC.rename(columns={1:'ETH Price Close', 3:'ETH Price High', 5:'ETH Price Low', 7:'ETH Price Open'}, inplace=True)
ETH_OHLC.drop([0,2,4,6], axis=1, inplace=True)
ETH_OHLC['ETH Price Close'] = ETH_OHLC['ETH Price Close'].apply(lambda x: float(str(x).replace(',',  '')))
ETH_OHLC['ETH Price High'] = ETH_OHLC['ETH Price High'].apply(lambda x: float(str(x).replace(',',  '')))
ETH_OHLC['ETH Price Low'] = ETH_OHLC['ETH Price Low'].apply(lambda x: float(str(x).replace(',',  '')))
ETH_OHLC['ETH Price Open'] = ETH_OHLC['ETH Price Open'].apply(lambda x: float(str(x).replace('}',  '')))
ETH_delta = ETH_OHLC['ETH Price Close'].diff(1)
ETH_delta.dropna(inplace=True)
ETH_gain = ETH_delta.copy()
ETH_loss = ETH_delta.copy()
ETH_gain[ETH_gain < 0] = 0
ETH_loss[ETH_loss > 0] = 0
time_period = 14
avg_ETH_gain = ETH_gain.rolling(window=time_period).mean()
avg_ETH_loss = abs(ETH_loss.rolling(window=time_period).mean())
ETH_RSI = 100.0 - (100.0 / (1 + (avg_ETH_gain / avg_ETH_loss)))
ETH.drop('ETH OHLC', axis=1, inplace=True)
ETH = ETH.append(ETH_OHLC)
ETH['ETH RSI'] = ETH_RSI

#BTC Realized Capitalization
#Realized capitalization is their average cost basis, valuing each bitcoin at the price of its last move.
#Whenever market cap drops below realized cap, the overall bitcoin market sells at a loss, denoting capitulation.
#Investor Capitalization discounts the capital paid to miners from the market’s general cost basis, serving as a bottom indicator in bear cycles.
#Investor capitalization = Realized Market Cap - Thermocap. Can be a good gauge of capitulation during bear markets.
#By removing the outstanding value paid to miners from the overall cost basis, we can assess the fair value of bitcoin at the bottom of a market cycle.
#Market cap tends to revert toward investor capitalization during bear markets and typically inflects when they near parity.

#RHODL is the ratio between the 1 week and the 1-2 years RCap HODL bands. In addition, it accounts for increased supply by weighting the ratio by the total market age.
#A high ratio is an indication of an overheated market and can be used to time cycle tops.

#Stock to Flow
#Stock to Flow is the ratio of the current stock of a commodity and the flow of new production.
#Stock to Flow Deflection is the ratio between the current Bitcoin price and the S/F model.
#If deflection is ≥ 1 it means that Bitcoin is overvalued according to the S/F model, otherwise undervalued.
BTC_S2F = BTC['BTC S2F'].str.split(n=- 1, expand=True)
BTC_S2F.rename(columns={1:'Days Till Halving', 3:'Ratio'}, inplace=True)
BTC_S2F.drop([0,2], axis=1, inplace=True)
BTC_S2F['Days Till Halving'] = BTC_S2F['Days Till Halving'].apply(lambda x: str(x).replace(',',  ''))
BTC_S2F['Ratio'] = BTC_S2F['Ratio'].apply(lambda x: str(x).replace('}',  ''))
BTC_S2F['Days Till Halving'] = BTC_S2F['Days Till Halving'].apply(lambda x: float(x))
BTC_S2F['Ratio'] = BTC_S2F['Ratio'].apply(lambda x: float(x))

BTC.drop('BTC S2F', axis=1, inplace=True)
BTC = BTC.append(BTC_S2F)

#BTC Coin Years Destroyed (CYD)
#An increase in cointime destroyed implies that holders are moving coins out of long-term storage and taking profits.
#At slightly above 5 billion today, coinyears destroyed we believe depicts a healthy bull market.
#Bitcoin’s price has hit more than triple its 2017 all-time high, and yet coinyears destroyed still is below the all-time high hit in early 2018.

#BTC RPV
#RPV ratio is realized on-chain profits divided by realized capitalization, measuring the difference between daily profit-taking behavior and buyers’ average cost basis.
#A ratio of 1 would indicate that every bitcoin is moving on that particular day.
#Historically, when profit-takers have moved 2% in one day, the market has hit a cyclical top.
#Conversely, when they have moved only 0.001% in one day, the market has been in the process of bottoming.
#After reaching levels of exuberance slightly below 2 earlier this year, followed by the 53% drop in the bitcoin price, the RPV ratio has reset to much healthier levels, as shown below.

#BTC Supply in Profit and Loss
#When the number of bitcoins in loss >= the number of bitcoins in profit, the prices have been in a bottoming process.

#BTC STH-SOPR
#STH-SOPR ratio of 1 typically is associated with local bottoms in bull markets and local tops in bear markets.
#When the ratio is below 1, in the aggregate market participants who have moved coins in the last 155 days have losses.
#Conversely, when the ratio is above 1, short-term participants have an aggregate gain. When selling off around a ratio of 1, bitcoin typically has entered a bear market.
#After bitcoin’s 53% correction from $63,000 USD to roughly $30,000 this past spring, its STH P/L ratio stabilized around 1, as shown below, suggesting that it was bottoming out. Today, STH P/L stands at 52, a value indicative of a potential local top.
#SOPR > 1 implies that the coins moved that day are, on average, selling at a profit.
#SOPR < 1 implies that the coins moved that day are, on average, selling at a loss.
#SOPR = 1 implies that the coins moved that day are, on average, selling coins at break even.
#SOPR trending higher implies profits are being realised with potential for previously illiquid supply being returned to liquid circulation
#SOPR trending lower implies losses are being realised and/or profitable coins are not being spent.

#MVRV and MVRV Z-Score
#MVRV ratio gives an indication of when the traded price is below a "fair value".
#When market value is significantly higher than realized value, it has historically indicated a top the opposite has indicated bottoms.
#MVRV Z-Score is (market cap – realized cap) / std(market cap).
#When MVRV < 1, the market is selling at a loss, which historically marked bottoms.
#When market cap rises dramatically relative to average cost, bitcoin typically is poised for large-scale profit-taking.
#Historically, bitcoin has topped out when the MVRV > 10.

#MVTV
#MVTV Ratio can be used to assess if currently trading at a premium with respect to total security spend by miners.
#MVTV ratio resembles the EV-to-EBITDA. MVTV compares investors’ current market cap to miners’ cash flow.
#Like MVRV, the MVTV ratio suggested last April that, at $63,000, bitcoin was in a strong bull trend but not near a blowoff.
#The price of bitcoin has since recovered from its 50% drawdown, with MVTV also nearing its previous local high.

#ETH DEF

#ETH Network

#ETH Trading
#NVT Ratio is market cap divided by the transferred on-chain volume.
#NVT Signal is a modified version of the NVT Ratio. It uses a 90 day moving average of the daily transaction volume.

writer = pd.ExcelWriter(r'C:\Users\amind\Juptyer lab Projects\Crypto Project\Glassnode Data.xlsx')
BTC.to_excel(writer, 'BTC')
ETH.to_excel(writer,'ETH')
writer.save()