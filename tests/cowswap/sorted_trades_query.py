import pandas as pd

from datastreams.datastream import Streamer

# ==============================================
# Run a query to fetch sorted trades schema data from the Cowswap subgraph.
# ==============================================

endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'

# instantiate Streamer object
ds = Streamer(endpoint)

# get a query field path from the query dictionary which is automatically populated in the Streamer object
field_path = ds.queryDict.get('trades')

# add parameters to the query_path
query_path = field_path(
    first=105,
    orderBy='timestamp',
    orderDirection='desc',
    where = {'timestamp_lt': 1650000000}
    )

# run query
df = ds.runQuery(query_path)

print(f'query returned {len(df)} rows')
print(df.head(10))
print(df.tail(10))
print('test finished')