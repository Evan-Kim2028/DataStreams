from dataclasses import dataclass
from datastreams.streamer import Streamer

from subgrounds.subgrounds import Subgrounds
from subgrounds.subgraph.subgraph import Subgraph

@dataclass
class DataStream:
    """
    Use DataStream to interface with the Streamer class. Future direction of the class is undecided. 
    The only benefit is abstracting away the execution layer from Streamer class. 

    Tentatively DataStream should store execution functionality whereas Streamer will store
    the subgraph interface functionality. 

    Additionally, Streamer should only interact with a single endpoint whereas DataStream can interact 
    multiple endpoints.
    """

    # Subgrounds is unique for every DataStream?
    def getDataStream(self, endpoint: str):
        """
        getDataStream is a firehose that returns all data from a subgraph endpoint.
        """
        # create new Subgrounds object
        sub = Subgrounds()
        # load subgraph data into Subgrounds
        subgraph = sub.load_subgraph(endpoint)

        # load Subgrounds data into Streamer
        streamer = Streamer(sub, endpoint, subgraph)

        # run Streamer. By default runStreamer is a firehose.
        streamer.runStreamer()
