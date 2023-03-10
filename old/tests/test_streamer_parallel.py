from datastreams.streamer import Streamer

# Run Streamer over a list of subgraph IDs
# endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'


ds = Streamer(endpoint)

# get values of endpoint after the last /
subgraph_name = ds.endpoint.split('/')[-1]

print(f'\nTHE ENDPOINT IS {subgraph_name}\n')

# ======================================================================================
# print(f'The schema list is initialized at startup and is:\n')
# for i in range(len(ds.schema)):
#     print(f'{ds.schema[i]}, type: {type(ds.schema[i])}')
# ======================================================================================
# filter_schema = ds.filterSchemaFields()
# print(f'\n#2) The filtered schema list with length {len(filter_schema)} is:')
# for i in range(len(filter_schema)):
#     print(f'{filter_schema[i]}, type: {type(filter_schema[i])}')

# query_schema = ds.getSchemaQueryFields()
# print(f'\n\n#3) The filtered query list with length {len(query_schema)} is:')
# for i in range(len(query_schema)):
#     print(f'{query_schema[i]}, type: {type(query_schema[i])}')
# ======================================================================================

# print(f'Non-Parallel Streamer Loop')
# ds.runStreamerLoop(query_size=13)

print(f'Parallel Streamer Loop')
query_list = ds.queryFields
ds.runStreamerLoopParallel(query_list=query_list, query_size=5)

# conver queryFields list to a list of strings
# query_list = [str(field) for field in ds.queryFields]

# maybe turn ds.queryFields and ds.queryStrs into a Streamer.dict var?
print(ds.queryFields)
print(ds.queryStrs)




print("\n\nscript is FINISHED")
