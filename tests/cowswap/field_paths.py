import pandas as pd

from datastreams.datastream import Streamer

# ==============================================
# Run to check the available fieldpaths for querying.
# ==============================================

endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'

# instantiate Streamer object
ds = Streamer(endpoint)

# print queryable schema dict keys. These are strings that map 1:1 to the corresponding fieldpath names.
print('Queryable Schema\n\n', ds.queryDict.keys())


print('test finished')