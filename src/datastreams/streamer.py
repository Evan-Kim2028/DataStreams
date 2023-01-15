import concurrent.futures
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
    :param list queryStrs: list of query strings. Default is `None`


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
    queryStrs: list[str] = None
    
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

        self.queryStrs = filtered_query_field_paths

        # convert str -> FieldPath
        filtered_query_field_paths = [self.getFieldPath(field) for field in filtered_query_field_paths]
        return filtered_query_field_paths

    def addSearchParam(self, query_field: FieldPath, search_param: dict, query_size = 10) -> FieldPath:
        """
        :param FieldPath query_field: FieldPath object
        :param int query_size: number of query results to return. Default is 10.
        :param dict search_param: search parameter to add to query
        :return: FieldPath object

        addSearchParam() is a helper function that adds a search parameter to a query.
        """

        return query_field(first=query_size, where=search_param)

    def runQuery(self, query_field: FieldPath, query_size: int=4, where=None) -> DataFrame:
        """
        :param FieldPath query_field: FieldPath object
        :param int query_size: number of query results to return. Default is 4.
        :param dict where: where is a dictionary conditional that specifies query searches. Default is None.
        :return: DataFrame object

        setupQuery() is a helper function that returns a DataFrame object for a query.
        """
        print(f'FIELD - {query_field}')

        if where == None:
            df = self.sub.query_df(query_field(query_size=query_size))
            return df
        else:
            print(f'Search query for these params!: {where}')
            query_field = self.addSearchParam(query_field, where, query_size=query_size) # add where condition to query_field
            df = self.sub.query_df(query_field)
            return df


    # def buildFunction(self):
    #     """
    #     Run multiple searches on a single FieldPath
    #     """



        
    def runStreamerLoop(self, query_size: int = 10, where=None) -> list[DataFrame]:
        """
        *SOFT DEPRECATION* - use runStreamerLoopParallel() instead. This function is left in for legacy purposes.

        :param int query_size: number of query results to return. Default is 10.
        :return: list of dataframes

        runStreamer() runs through ALL queryable fields list and returns a list of query dataframes. 
        """
        # create empty dictionary to store query data
        df_data = []

        #start time
        start_time = time.time()
        for i in range(len(self.queryFields)):
            df = self.runQuery(self.queryFields[i], query_size)
            df_data.append(df)
        # end time
        end_time = time.time() - start_time
        
        print(f'{len(self.queryFields)} queries, single core: {end_time:.2f} seconds. Largest df is {len(max(df_data, key=len))}\n')
        return df_data

    def runStreamerLoopParallel(self, query_list: list[FieldPath], query_size: int = 10, cores: int = 4) -> list[DataFrame]:
        """
        :param list[FieldPath] query_list: list of FieldPath objects
        :param int query_size: number of query results to return. Default is 10.
        :param int cores: number of cores to use. Default is 4.
        :return: list of dataframes

        runStreamer() runs through ALL queryable fields list and returns a list of query dataframes.
        """
        # create a list of tuples between query_size and query_list
        query_list = [(query, query_size) for query in query_list]
        df_data = []

        start_time = time.time()
        # Create a pool of 4 worker processes   
        with concurrent.futures.ThreadPoolExecutor(max_workers=cores) as executor:
            # Calculate the square of each number in parallel
            for args in query_list:
                future = executor.submit(self.runQuery, *args)
                df_data.append(future.result())

        end_time = time.time() - start_time
        print(f'{len(self.queryFields)} queries, parallelized 4 cores: {end_time:.2f} seconds. Largest df is {len(max(df_data, key=len))}\n')

        return df_data


