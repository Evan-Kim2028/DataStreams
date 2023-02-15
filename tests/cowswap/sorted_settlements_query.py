import pandas as pd

from datastreams.datastream import Streamer
# maximize row width to see tx ids
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)


# ==============================================
# Run a query to fetch sorted settlements schema data from the Cowswap subgraph.
# ==============================================

endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'

# instantiate Streamer object
ds = Streamer(endpoint)

# get a query field path from the query dictionary which is automatically populated in the Streamer object
field_path = ds.queryDict.get('settlements')

# add parameters to the query_path.
query_path = field_path(
    first=105,
    orderBy='firstTradeTimestamp',
    orderDirection='desc',
    where = {'firstTradeTimestamp_lt': 1650000000} 
    )

# run query
df = ds.runQuery(field_path)

print(f'query returned {len(df)} rows')
print(df.head(10))
print(df.tail(10))
print('test finished')