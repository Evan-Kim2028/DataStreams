import pandas as pd

from datastreams.datastream import Streamer

# ==============================================
# Run a query to fetch 150 trades from the Cowswap subgraph unsorted.
# ==============================================

endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'

# instantiate Streamer object
ds = Streamer(endpoint)

# define a query field path
query_path = ds.queryDict.get('trades')

# run query
df = ds.runQuery(query_path, query_size=150)

print(df.head(5))

print('test finished')