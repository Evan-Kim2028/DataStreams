from datastreams.streamer import Streamer
from subgrounds.subgrounds import Subgrounds

# Run a sample Streamer
hosted_query_ids = [
                'https://api.thegraph.com/subgraphs/name/cowprotocol/cow',
                'https://api.thegraph.com/subgraphs/name/cowprotocol/cow-gc'
                ]

sub_firehose_data = []
counter = 0
for endpoint in hosted_query_ids:
    counter += 1
    print(f'query {counter} for {endpoint}')
    sub = Subgrounds()
    subgraph = sub.load_subgraph(endpoint)
    dataStreamer = Streamer(sub, endpoint, subgraph)
    dataStreamer.runStreamer()
    sub_firehose_data.append(dataStreamer)