import pandas as pd

from datastreams.datastream import Streamer

# ==============================================
# Run a query to fetch sorted swaps schema data from Univ3 Ethereum subgraph.
# ==============================================

endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'

# instantiate Streamer object
ds = Streamer(endpoint)

# get a query field path from the query dictionary which is automatically populated in the Streamer object
field_path = ds.queryDict.get('swaps')

# add parameters to the query_path.
query_path = field_path(
    first=105,
    orderBy='timestamp',
    orderDirection='desc',
    where = {'timestamp_lt': 1650000000} 
    )

# run query
df = ds.runQuery(field_path)

trunc_df = df[[
    'swaps_hash', 
    'swaps_blockNumber', 
    'swaps_timestamp', 
    'swaps_tokenIn_id',
    'swaps_tokenOut_id',
    'swaps_amountIn',
    'swaps_amountOut',
    'swaps_amountInUSD',
    'swaps_amountOutUSD',
    ]]

print(f'query returned {len(df)} rows. df columns are {df.columns}')
print(trunc_df.head(10))
print(trunc_df.tail(10))
print('test finished')