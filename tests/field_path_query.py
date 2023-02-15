import pandas as pd

from datastreams.datastream import Streamer

# ==============================================
# Test runQuery method.


# ==============================================
# endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum'

# instantiate Streamer object
ds = Streamer(endpoint)

# print queryable schema dict keys. These are strings that map 1:1 to the corresponding fieldpath names.
print('Queryable Schema\n\n', ds.queryDict.keys())

# define a query field path
query_path = ds.queryDict.get('swaps')

# run query
df = ds.runQuery(query_path, query_size=150)

print(df.head(5))

print('test finished')