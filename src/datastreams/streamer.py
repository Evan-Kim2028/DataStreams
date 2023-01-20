import concurrent.futures
import time

from dataclasses import dataclass

from subgrounds.pagination.pagination import PaginationError
from subgrounds.subgraph.subgraph import Subgraph
from subgrounds.subgrounds import Subgrounds
from subgrounds.subgraph.fieldpath import FieldPath


from pandas import DataFrame

@dataclass
class Streamer:
    """
    Streamer is a query utility class that makes queries easier to define and build queries using Subgrounds functions. 
    Streamer makes it easier to define query paths by introducing helper functions that expose commonly used 
    Subgrounds functions. Each Streamer relates  to a single subgraph. Introducing these helper functions allows Streamer to queue up multiple queries of different parts of a schema at once. 

    :param Subgrounds sub: Subgrounds object. Default is `None`
    :param str endpoint: graphql endpoint. Default is `None`
    :param Subgraph subgraph: Subgraph object. Default is `None`
    :param list data: list of dataframes. Default is `None`
    :param list schema: list of schema objects. Default is `None`
    :param list queryFields: list of queryable fields. Default is `None`
    :param list queryStrs: list of query strings. Default is `None`
    :param dict queryDict: dictionary of query strings. Default is `None`
    """

    endpoint: str = None
    subgraph: Subgraph = None
    sub: Subgrounds = None
    data: list = None
    schema: list = None
    queryFields: list = None
    queryStrs: list[str] = None 
    queryDict: dict = None
    
    def __post_init__(self):
    # Perform startup tasks here
        self.setupStreamer()
        self.schema = self.getSubgraphSchema()
        self.queryStrs = self.filterQueryFieldStrs()
        self.queryFields = self.filterQueryFields()
        self.queryDict = self.getQueryDict()

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
        getFieldPath converts a string to a FieldPath object. In a Subgrounds query, the format follows subgrounds.schema.FieldPath.

        :param str field: Enter the string that will be converted to a FieldPath
        :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used. 
        :return: FieldPath object
        """
        return self.subgraph.__getattribute__(operation).__getattribute__(field)

    def getSubgraphSchema(self) -> list[str]:
        """
        getSubgraphSchema gets the schema list from a Subgraph.

        :return: schema list from a Subgraph
        """
        return list(name for name, type_ in self.subgraph._schema.type_map.items() if type_.is_object)

    def getSchemaFields(self, schema_object: str) -> list[str]:
        """
        getSubgraphField gets a fields list from a subgraph schema.

        :param str schema_object: Schema object name to get fields list from
        :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used.
        :return: strings field list from a Subgraph schema
        """
        return list(field.name for field in self.subgraph.__getattribute__(schema_object)._object.fields)

    def getQueryFields(self) -> list[str]:
        """
        Get all queryable fields from the subgraph schema.

        :return: list[str] of queryable fields from the subgraph schema
        """
        query_field_paths = self.getSchemaFields(self.schema[self.schema.index('Query')])
        # print(f'query field paths for this {len(query_field_paths)} length schema are {query_field_paths}')

        return query_field_paths

    def filterQueryFieldStrs(self) -> list[str]:
        """
        filterQueryFieldStrs() is an inner helper function run at startup that stores a str representation of the queryable fields.

        :return: list[str] of queryable fields
        """
        # get query field list
        query_field_paths = self.getQueryFields()

        filtered_query_field_paths = [field for field in query_field_paths if field.endswith('s')]

        # filter out None values
        filtered_field_paths_str = list(filter(None, filtered_query_field_paths))

        return filtered_field_paths_str

    def filterQueryFields(self) -> list[FieldPath]:
        """
        filterQueryFields() is an inner helper function run at startup that stores a FieldPath representation of the queryable fields.

        :return: list[FieldPath] of queryable fields
        """
        # convert str -> FieldPath
        filtered_field_paths= [self.getFieldPath(field) for field in self.queryStrs]

        return filtered_field_paths

    def getQueryDict(self):
        """
        getQueryDict() is an inner helper function run at startup that stores a dictionary of queryable fields in {str: FieldPath} format. 
        This function allows the subgraph schema to be searchable by dictionary keys.

        :return: dict of queryable fields in {str: FieldPath} format
        """
        query_dict = dict(zip(self.queryStrs, self.queryFields))

        return query_dict
        
    def addSearchParam(self, query_field: FieldPath, search_param: dict, query_size = 10, order_Direction: str ='desc') -> FieldPath:
        """
        addSearchParam() adds an optional search parameter to a Subgraph query.

        :param FieldPath query_field: FieldPath object
        :param int query_size: number of query results to return. Default is 10.
        :param dict search_param: search parameter to add to query
        :param str order_Direction: order direction for query. Default is 'desc'
        :return: FieldPath object
        """

        return query_field(first=query_size, where=search_param, orderDirection='desc')

    def runQuery(self, query_field: FieldPath, query_size: int=4, where=None) -> DataFrame:
        """
        setupQuery() returns a DataFrame object from a Subgraph query.

        :param FieldPath query_field: FieldPath object
        :param int query_size: number of query results to return. Default is 4.
        :param dict where: where is a dictionary conditional that specifies query searches. Default is None.
        :return: DataFrame object
        """
        print(f'FIELD - {query_field}')
        if where == None:
            df = self.sub.query_df(query_field(first=query_size))
            # add endpoint column to df
            df['endpoint'] = self.endpoint
            return df
        else:
            print(f'Filter based on these values: {where}')
            query_field = self.addSearchParam(query_field, where, query_size=query_size) # add where condition to query_field
            df = self.sub.query_df(query_field)
            df['endpoint'] = self.endpoint
            return df

    def runSameQuerySearch(self, fieldParam: FieldPath, keys: list[str], values: list, searchKey: str, searchVals: list, query_size: int = 10) -> list[DataFrame]:
        """
        runSameQuerySearch() allows a user to search for multiple values within the same query field schema.

        :param FieldPath fieldParam: FieldPath object
        :param list[str] keys: list of keys to search
        :param list values: list of values to search
        :param str searchKey: key to search for
        :param list searchVals: list of values to search for
        :param int query_size: number of query results to return. Default is 10.
        :return: list[DataFrame] object
        """
        df_data = []

        search_dict = dict(zip(keys, values))
        print(f'search_dict: {search_dict}') # debugging

        # change the pair value to the search value
        for val in searchVals:
            print(f'val: {val}') # debugging
            search_dict[searchKey] = val
            df = self.runQuery(fieldParam, where=search_dict, query_size=query_size)
            df_data.append(df)
            print(val, df)

        return df_data

    def runStreamerSearchParallel(self, fieldParam: FieldPath, keys: list[str], values: list, searchKey: str, searchVals: list, cores: int = 4, query_size: int = 10) -> list[DataFrame]:
        """
        runStreamerSearchParallel is a parallelized version of runSameQuerySearch. Parameter input is the same.

        :param FieldPath fieldParam: FieldPath object
        :param list[str] keys: list of keys to search
        :param list values: list of values to search
        :param str searchKey: key to search for
        :param list searchVals: list of values to search for
        :param int cores: number of cores to use for parallelization. Default is 4.
        :param int query_size: number of query results to return. Default is 10.
        :return: list[DataFrame] object
        """
        search_dict = dict(zip(keys, values))

        print(f'search_dict: {search_dict}') # debugging

        # make query_list
        query_list = []
        for val in searchVals:
            # update search_dict[searchKey] with new value
            search_dict[searchKey] = val

            # make a list of args for parallelization
            print(f'search_dict: {search_dict[searchKey]}')
            print(f'val: {val}') # debugging
            query_list.append((fieldParam, search_dict, query_size))
        # print(f'query_list: {query_list}') # debubbing

        df_data = []
        # Create a pool of 4 worker processes   
        with concurrent.futures.ThreadPoolExecutor(max_workers=cores) as executor:
            # Calculate the square of each number in parallel
            for args in query_list:
                future = executor.submit(self.runQuery, *args)
                df_data.append(future.result())
        return df_data

    def runStreamerLoop(self, query_field_list: list[FieldPath], query_size: int = 10, where=None) -> list[DataFrame]:
        """
        *SOFT DEPRECATION* - use runStreamerLoopParallel() instead. This function is left in for legacy purposes.
        runStreamer() runs through a list of queryable fields list and returns a list of Subgraph query dataframes. 

        :param list[FieldPath] query_field_list: list of FieldPath objects
        :param int query_size: number of query results to return. Default is 10.
        :param dict where: where is a dictionary conditional that specifies query searches. Default is None.
        :return: list of dataframes
        """
        # create empty dictionary to store query data
        df_data = []

        #start time
        start_time = time.time()
        for i in range(len(query_field_list)):
            try:
                df = self.runQuery(query_field_list[i], query_size)
                df_data.append(df)
            except PaginationError as e:
                print(f'Caught error: {e} with queryField: {query_field_list[i]}. Moving on anyways...')
                pass
        # end time
        end_time = time.time() - start_time
        
        print(f'{len(query_field_list)} queries, single core: {end_time:.2f} seconds. Largest df is {len(max(df_data, key=len))}\n')
        return df_data

    def runStreamerLoopParallel(self, query_list: list[FieldPath], query_size: int = 10, cores: int = 4) -> list[DataFrame]:
        """
        runStreamerLoopParallel() runs through a list of queryable fields and returns a list of Subgraph query dataframes.

        NOTE - This function does not support parallelized search filter queries.

        :param list[FieldPath] query_list: list of FieldPath objects
        :param int query_size: number of query results to return. Default is 10.
        :param int cores: number of cores to use. Default is 4.
        :return: list of dataframes
        """
        # create a list of tuples between query_size and query_list
        query_list = [(query, query_size) for query in query_list]
        df_data = []

        start_time = time.time()
        # Create a pool of 4 worker processes   
        with concurrent.futures.ThreadPoolExecutor(max_workers=cores) as executor:
            # Calculate the square of each number in parallel
            for args in query_list:
                try:
                    future = executor.submit(self.runQuery, *args)
                    df_data.append(future.result())
                except PaginationError as e:
                    print(f'Caught error: {e} with args: {args}. Moving on anyways...')
                    pass
        end_time = time.time() - start_time
        print(f'{len(self.queryFields)} queries, parallelized 4 cores: {end_time:.2f} seconds. Largest df is {len(max(df_data, key=len))}\n')

        return df_data


