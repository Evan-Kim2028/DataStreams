from datastreams.datastream import DataStream


ds = DataStream()

endpoint_ids = [
                'https://api.thegraph.com/subgraphs/name/cowprotocol/cow',
                'https://api.thegraph.com/subgraphs/name/cowprotocol/cow-gc'
                ]


# test getDataStream() functionality in a loop
for endpoint in endpoint_ids:
    ds.getDataStream(endpoint)

