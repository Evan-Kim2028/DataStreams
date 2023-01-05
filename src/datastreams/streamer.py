import os
import time

from dataclasses import dataclass
from subgrounds.subgraph.subgraph import Subgraph
from subgrounds.subgrounds import Subgrounds
from subgrounds.subgraph.fieldpath import FieldPath

from pandas import DataFrame

@dataclass
class Streamer:
    """
    :param Subgrounds sub: Subgrounds object. Default is `None`
    :param str endpoint: graphql endpoint. Default is `None`
    :param Subgraph subgraph: Subgraph object. Default is `None`
    :param list data_list: list of dataframes. Default is `None`
    :param list schema: list of schema objects. Default is `None`
    :param list queryFields: list of queryable fields. Default is `None`


    Streamer is a query utility class that makes queries easier to define and build queries using Subgrounds functions. 
    Streamer makes it easier to define query paths by introducing helper functions that expose commonly used 
    Subgrounds functions. Each Streamer relates  to a single subgraph.
    
    Introducing these helper functions allows Streamer to queue up multiple queries of different parts of a schema at once. 
    The data flow can be described as follows:

    #. Load Subgraph -  Load the schema field list from a graphql endpoint. The field list loaded defaults to the 'Query' schema. 
    #. Define Query Path - Streamer allows you to define a query path and queue up multiple queries of different parts of the schema at once.
    #. The query path is defined automatically to run every possible query on the subgraph and returns a list of dataframes.
    """

    endpoint: str = None
    subgraph: Subgraph = None
    sub: Subgrounds = None
    data: list = None
    schema: list = None
    queryFields: list = None
    
    def __post_init__(self):
    # Perform startup tasks here
        self.setupStreamer()
        self.schema = self.getSubgraphSchema()
        self.queryFields = self.filterQueryFields()

    def setupStreamer(self):
        """
        run this function when Streamer is initialized. This function initializes a Subgrounds object and loads a Subgraph object into Subgrounds.
        Since this is needed before doing anything with Subgrounds, this is done automatically at start to remove additional dependencies from using Streamer.
        """
        self.sub = Subgrounds()
        self.subgraph = self.sub.load_subgraph(self.endpoint)
        self.data = []
        self.schema = []

    def getFieldPath(self, field: str,  operation: str ='Query') -> FieldPath:
        """
        :param str field: Enter the string that will be converted to a FieldPath
        :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used. 
        :return: FieldPath object


        getFieldPath converts a string to a FieldPath object. In a Subgrounds query, the format follows subgrounds.schema.FieldPath.
        """
        return self.subgraph.__getattribute__(operation).__getattribute__(field)

    def getSubgraphSchema(self) -> list[str]:
        """
        :return: schema list from a Subgraph


        getSubgraphSchema gets the schema list from a Subgraph.
        """
        return list(name for name, type_ in self.subgraph._schema.type_map.items() if type_.is_object)

    def getSchemaFields(self, schema_object: str) -> list[str]:
        """
        :param str schema_object: Schema object name to get fields list from
        :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used.
        :return: strings field list from a Subgraph schema

        getSubgraphField gets a fields list from a subgraph schema.
        """
        return list(field.name for field in self.subgraph.__getattribute__(schema_object)._object.fields)

    def getQueryFields(self) -> list[str]:
        """
        :return: list[str] of queryable fields from the subgraph schema

        Get all queryable fields from the subgraph schema.
        """
        query_field_paths = self.getSchemaFields(self.schema[self.schema.index('Query')])
        # print(f'query field paths for this {len(query_field_paths)} length schema are {query_field_paths}')

        return query_field_paths

    def filterQueryFields(self) -> list[FieldPath]:
        """
        :return: list[FieldPath] of queryable fields that end with an 's'

        Filter fields that end with an 's'
        """

        # get query field list
        query_field_paths = self.getQueryFields()

        filtered_query_field_paths = [field for field in query_field_paths if field.endswith('s')]

        # filter out None values
        filtered_query_field_paths = list(filter(None, filtered_query_field_paths))

        # convert str -> FieldPath
        filtered_query_field_paths = [self.getFieldPath(field) for field in filtered_query_field_paths]
        return filtered_query_field_paths

    def runQuery(self, query_field: FieldPath, query_size: int=4) -> DataFrame:
        """
        :param FieldPath query_field: FieldPath object
        :param int query_size: number of query results to return. Default is 4.
        :return: DataFrame object

        setupQuery() is a helper function that returns a DataFrame object for a query.
        """
        print(f'FIELD - {query_field}')

        # 2) Run query
        df = self.sub.query_df(query_field(first=query_size))
        
        return df



    def runStreamerLoop(self) -> dict:
        """
        :return: list of dataframes

        runStreamer() runs through ALL queryable fields list and returns a list of query dataframes.
        """
        # create empty dictionary to store query data
        df_data = []

        for i in range(len(self.queryFields)):
            df = self.runQuery(self.queryFields[i])
            df_data.append(df)

        return df_data


