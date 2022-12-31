from datastreams.streamer import Streamer

# Run Streamer over a list of subgraph IDs
endpoint = 'https://api.thegraph.com/subgraphs/name/cowprotocol/cow'





ds = Streamer(endpoint)

print(f' the endpoint is {ds.endpoint}')

print(f'the schema list is {ds.schema_list}')

ds.runStreamer()

print("script is finished")