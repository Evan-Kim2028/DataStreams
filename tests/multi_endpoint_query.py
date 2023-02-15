from datastreams.datastream import DataStream

import pandas as pd

# list of Ethereum Dex endpoints
endpointList = [
    'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/curve-finance-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    ]


# instantiate DataStream object
ds = DataStream(endpointList)

# 2/15/23 TODO - Add fieldpath search params to the query batch???

# run batched queries
df_list = ds.querySubgraphs(ds.streamerDict, 'swaps')

# flatten list of DataFrames into one DataFrame
df = pd.concat(df_list, axis=0, ignore_index=True)


print(f'query returned {len(df)} rows. The columns are: {df.columns}')
print(df.head(10))
print(df.tail(10))
print('test finished')