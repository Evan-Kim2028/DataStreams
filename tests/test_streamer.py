import pandas as pd

from datastreams.datastream import Streamer


endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'
ds = Streamer(endpoint)

print('\n\n', ds.queryDict)

my_keys = ['trades', 'orders', 'settlements', 'tokens']

selected_values = [ds.queryDict.get(key) for key in my_keys]

print(f'\n\nselected field values: {selected_values}')

print('finished')