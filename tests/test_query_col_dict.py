from datastreams.datastream import Streamer

import pandas as pd

# select subgraph endpoint
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'
# USDC/WETH 
lp_name = '0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640'

# load Streamer class
ds = Streamer(endpoint)

field_path = ds.queryDict.get('liquidityPools')

col_query_list = ds.getFieldPathQueryCols(field_path)

col_query_dict = ds.getQueryCols(field_path, col_query_list)

print(col_query_dict['inputTokenBalances'])

df = ds.runQuery(col_query_dict['inputTokenBalances'], query_size=1000)

print(df)


print('FINISH TEST')