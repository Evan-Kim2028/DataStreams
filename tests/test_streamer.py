from datastreams.streamer import Streamer

# Run Streamer over a list of subgraph IDs
# endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'
endpoint = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'



ds = Streamer(endpoint)

print(f' The endpoint is:\n {ds.endpoint}\n')


print(f'The schema list is initialized at startup and is:\n')
for i in range(len(ds.schema)):
    print(f'{ds.schema[i]}')

# ds.runStreamer() # currently broken. being refactored 


filter_schema = ds.filterSchemaFields()
print(f'\nThe filtered schema list with length {len(filter_schema)}is:')
for i in range(len(filter_schema)):
    print(f'{filter_schema[i]}')

# [print(f'{val}') for val in filter_schema]
# print(f'The filtered schema list is:\n \n{[print(val) for val in filter_schema]}\n')



query_schema = ds.getSchemaQueryFields()
print(f'\nThe filtered query list with length {len(query_schema)} is:')
for i in range(len(query_schema)):
    print(f'{query_schema[i]}')

# [print(f'{val}') for val in query_schema]
# print(f'The filtered query list is:\n \n{[print(val) for val in query_schema]}\n')


print("\n\nscript is finished")

# Why is there event/helperStore in filtered query list but not filtered schema list??