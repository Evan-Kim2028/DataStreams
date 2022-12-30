from datastreams.datastream import DataStream


ds = DataStream()

ds.getDataStream('https://api.thegraph.com/subgraphs/name/cowprotocol/cow', 100000000)
