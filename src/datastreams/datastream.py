from dataclasses import dataclass
from datastreams.streamer import Streamer
from functools import reduce
from subgrounds.subgrounds import Subgrounds
from pandas import DataFrame

@dataclass
class DataStream:
    """
    DataStream is used to manage multiple Streamer objects. In other words, you can manage multiple Subgraph queries
    with DataStream.

    #. Insert a list of endpoints, each one represents a Subgraph endpoint.
    """
    endpointList: list[str] = None
    streamerDict: dict = None

    def __post_init__(self):
        self.makeStreamerDict()

    def makeStreamerDict(self):
        """
        generate streamerDict from endpointList
        """
        self.streamerDict: dict = {}

        for endpoint in self.endpointList:
            # generate the name from the endpoint as the string seperated by the right most /
            name = endpoint.split('/')[-1]
            # create new Streamer object
            streamer = Streamer(endpoint)
            # add to streamerDict dict
            self.streamerDict[name] = streamer

    def getCommonQueryKeys(self, streamerList: dict = None) -> list[str]:
        """
        getCommonQueryKeys returns a list of query keys that are common to all Streamer objects.

        :param list[Streamer] streamerList: list of Streamer objects. Default is None, which will use all Streamer objects in streamerDict
        """
        if streamerList:
            common_keys = list(reduce(set.intersection, [set(ds.queryDict.keys()) for ds in streamerList.values()]))
        else:
            common_keys = list(reduce(set.intersection, [set(ds.queryDict.keys()) for ds in self.streamerDict.values()]))

        return common_keys


    def querySubgraphs(self, streamer_dict: dict, query_field: str) -> list[DataFrame]:
        """
        query all Subgraphs in a streamer dictionary for a specific query field

        :param dict streamer_dict: dictionary of Streamer objects
        :param str query_field: query field to run
        """
        data = []
        #run query on streamer objects
        for ds in streamer_dict.values():
            print(f'querying {ds.endpoint} for {query_field}...')
            # 2.15.23 TODO - construct new query fieldpath here?

            # run batch queries
            tokens_df = ds.runQuery(ds.queryDict[query_field])
            data.append(tokens_df)
        return data



    # # Subgrounds is unique for every DataStream?
    # def getDataStream(self, endpoint: str):
    #     """
    #     :param str endpoint: graphql endpoint

    #     getDataStream is a firehose that returns all data from a subgraph endpoint.
    #     """
    #     # create new Subgrounds object
    #     sub = Subgrounds()
    #     # load subgraph data into Subgrounds
    #     subgraph = sub.load_subgraph(endpoint)

    #     # load Subgrounds data into Streamer
    #     streamer = Streamer(sub, endpoint, subgraph)

