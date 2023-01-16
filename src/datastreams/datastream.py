from dataclasses import dataclass
from datastreams.streamer import Streamer

from subgrounds.subgrounds import Subgrounds

@dataclass
class DataStream:
    """
    ** CURRENTLY BEING BUILT. NOT USABLE YET **
    Use DataStream to interface with the Streamer class. Future direction of the class is undecided. 
    The only benefit is abstracting away the execution layer from Streamer class. 

    Tentatively DataStream should store execution functionality whereas Streamer will store
    the subgraph interface functionality. 

    Additionally, Streamer should only interact with a single endpoint whereas DataStream can interact 
    multiple endpoints.
    """

    # Subgrounds is unique for every DataStream?
    def getDataStream(self, endpoint: str, query_size = 5):
        """
        :param str endpoint: graphql endpoint
        :param int query_size: number of queries to run. Default is 5.


        getDataStream is a firehose that returns all data from a subgraph endpoint.
        Should query_size, a graphQl parameter be contained in this function? Or moved somewhere else
        """
        # create new Subgrounds object
        sub = Subgrounds()
        # load subgraph data into Subgrounds
        subgraph = sub.load_subgraph(endpoint)

        # load Subgrounds data into Streamer
        streamer = Streamer(sub, endpoint, subgraph)

        # run Streamer. By default runStreamer is a firehose.
        streamer.runStreamer(query_size)
