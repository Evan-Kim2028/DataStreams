from datastreams.datastream import DataStream



endpointList = [
    'https://api.thegraph.com/subgraphs/name/messari/sushiswap-ethereum', 
    'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/curve-finance-ethereum',
    'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2', # https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v2 # NON-MESSARi SUBGRAPH
    'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    'https://api.thegraph.com/subgraphs/name/messari/saddle-finance-ethereum'
    ]



ds = DataStream(endpointList)

# endpoints loaded into DataStream
print(f' the endpoints are: {ds.streamerDict.keys()}')

# check the keys for a single Streamer "sushiswap-ethereum"
# print(ds.streamerDict['sushiswap-ethereum'].queryDict.keys())

common_keys = ds.getCommonQueryKeys()
print(f'common_keys: {common_keys}') # the common_keys are very small because uniswap-v2 is not a messari standardized subgraph.

# make a new streamerDict excluding uniswap-v2
new_dict = ds.streamerDict
new_dict.pop('uniswap-v2')


new_common_keys = ds.getCommonQueryKeys(streamerList=new_dict)
print(f'new_common_keys: {new_common_keys}') # we now have a much larger list of common keys after dropping uniswap-v2

tokens_dfs = ds.querySubgraphs(new_dict, 'tokens', query_size=7)
print(tokens_dfs)



print('FINISHED')