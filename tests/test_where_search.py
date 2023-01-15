from datastreams.datastream import Streamer
import pandas as pd

endpoint = 'https://api.thegraph.com/subgraphs/name/openpredict/chainlink-prices-subgraph'

ds = Streamer(endpoint)


print(f'#1) - query fields: {ds.queryFields}')


search_eth = {'timestamp_lt': 1663907363, 'assetPair': "ETH/USD"}
search_btc = {'timestamp_lt': 1663907363, 'assetPair': "BTC/USD"}

df = ds.runQuery(ds.queryFields[0], where=search_eth, query_size=102)
# df = ds.runQuery(ds.queryFields[0], query_size=102)


print(df.head(5))


print('finished')