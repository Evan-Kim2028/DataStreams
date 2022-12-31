from datastreams.streamer import Streamer

# Run Streamer over a list of subgraph IDs
endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'





ds = Streamer(endpoint)

print(f' The endpoint is:\n {ds.endpoint}\n')

print(f'The schema list is initialized at startup and is:\n \n{ds.schema}\n')

# ds.runStreamer() # currently broken. being refactored 

li_one, li_two = ds.filterSchema()

print(f'The filtered schema list is:\n \n{li_one}\n')
print(f'The filtered query list is:\n \n{li_two}\n')

print("script is finished")