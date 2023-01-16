from datastreams.datastream import Streamer
import pandas as pd

endpoint = 'https://api.thegraph.com/subgraphs/name/openpredict/chainlink-prices-subgraph'

ds = Streamer(endpoint)


print(f'#1) - query fields: {ds.queryFields}')

keys = ['timestamp_lt', 'assetPair']
initial_vals = [1673800967, 'ETH/USD']

search_vals = ["ETH/USD", "BTC/USD", "LINK/USD", "UNI/USD"]


dfs = ds.runSameQuerySearch(
    fieldParam = ds.queryFields[0],
    keys = keys, 
    values = initial_vals,
    searchKey = keys[1],
    searchVals = search_vals,
    query_size = 101
    )

print(dfs)

# parallel doesn't work, getting type error
# dfs_parallel = ds.runStreamerSearchParallel(
#     fieldParam = ds.queryFields[0],
#     keys = keys, 
#     values = values,
#     searchKey = keys[1],
#     searchVals = search_vals,
#     query_size = 101
#     )

# print(dfs_parallel)

print('finished')