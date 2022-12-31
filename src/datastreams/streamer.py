import os
import time

from dataclasses import dataclass, field
from subgrounds.subgraph.subgraph import Subgraph
from subgrounds.schema import TypeRef
from subgrounds.subgrounds import Subgrounds
from subgrounds.subgraph.fieldpath import FieldPath


@dataclass
class Streamer:
    """
    :param Subgrounds sub: Subgrounds object
    :param str endpoint: graphql endpoint
    :param Subgraph subgraph: Subgraph object
    :param list data_list: list of dataframes. default is []
    :param list schema_list: list of schema objects. default is []


    Streamer is a query utility class that makes queries easier to define and build queries using Subgrounds functions. 
    Streamer makes it easier to define query paths by introducing helper functions that expose commonly used 
    Subgrounds functions. 
    
    Introducing these helper functions allows Streamer to queue up multiple queries of different parts of a schema at once. 
    The data flow can be described as follows:

    #. Load Subgraph -  Load the schema field list from a graphql endpoint. The field list loaded defaults to the 'Query' schema. 
    #. Define Query Path - Streamer allows you to define a query path and queue up multiple queries of different parts of the schema at once.
    #. The query path is defined automatically to run every possible query on the subgraph and returns a list of dataframes.
    """

    sub: Subgrounds
    endpoint: str
    subgraph: Subgraph
    data_list: list = field(default_factory=list) 
    schema_list: list = field(default_factory=list) 


    def getFieldPath(self, subgraph: Subgraph, field: str,  operation: str ='Query') -> FieldPath:
        """
        :param Subgraph subgraph: Subgraph object with a loaded graphql endpoint
        :param str field: Enter the string that will be converted to a FieldPath
        :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used. 
        :return: FieldPath object


        getFieldPath converts a string to a FieldPath object.
        """
        return subgraph.__getattribute__(operation).__getattribute__(field)

    def getSubgraphSchema(self, subgraph: Subgraph) -> list[str]:
        """
        :param Subgraph subgraph: Subgraph object with a loaded Subgraph endpoint
        :return: schema list from a Subgraph


        getSubgraphSchema gets the schema list from a Subgraph.
        """
        return list(name for name, type_ in subgraph._schema.type_map.items() if type_.is_object)

    def getSchemaFields(self, subgraph: Subgraph, schema_object: str) -> list[str]:
        """
        :param Subgraph subgraph: Subgraph object with a loaded graphql endpoint
        :param str schema_object: Schema object name to get fields list from
        :param str operation: Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used.
        :return: strings field list from a Subgraph schema


        getSubgraphField gets a fields list from a subgraph schema.
        """
        return list(field.name for field in subgraph.__getattribute__(schema_object)._object.fields)

    def formatFieldStr(self, field: str) -> str:
        """
        :param str field: field string
        :return: formatted field string that has been parsed to match the predicted query string


        formatFieldStr formats the field string to match the query string. In order to make the field string queryable, if value does 
        not end with a s and does not start and end with _, make the first non _ character in the string a capital letter.

        CAUTION - this is a heuristic method. There is no Subgraph common naming convention so this heuristic will not always work. In future work,
        it would be worthwhile to add more functionality to make this method more robust and/or robust. 
        """
        if not field.endswith('s') and not field.startswith('_'):
            field = field[0].upper() + field[1:]
        return field

    def runStreamer(self, query_size: int =5):
        """
        :param int query_size: number of results to return for each query. default is 5


        runStreamer() gets all queryable fields from a subgraph from every schema. The list of dataframes is stored in the Streamer data_list.
        Set the query_size to the number of results you want to return for each query. Default is 5. There are currently
        four steps in runStreamer():
        #. get schema list 
        #. get schema query field list
        #. filter, format, and sort. End result is subgraph_query_field_list -> sorted_subgraph_field_query_list steps
        #. order the field and schema lists

        TODO - break this function down into four sub functions? Probably a good idea.
        """

    # 1) get schema list 
        schema_list = self.getSubgraphSchema(self.subgraph)

    # 2) get schema query field list
        query_field_list = self.getSchemaFields(self.subgraph, schema_list[schema_list.index('Query')])

    # 2) filter, format, and sort. End result is subgraph_query_field_list -> sorted_subgraph_field_query_list steps
        filtered_schema_list = [x for x in schema_list if not x.endswith('_') and x != 'Query' and x != 'Subscription']
        # format query fields
        fmt_query_field_list = [self.formatFieldStr(field) for field in query_field_list]
        # drop empty values if there are any. Empty fields will break the query.
        fmt_query_field_list = [field for field in fmt_query_field_list if field != '']
        # make a query field list with queryable fields - these are plural values that end with 's'.
        subgraph_query_field_list = [field for field in fmt_query_field_list if field.endswith('s')]
        # make a subgraph schema list with schema objects that relate to the query fields. These are singular values that do not end with 's'.
        subgraph_schema_query_list = [field[0].upper() + field[1:] for field in filtered_schema_list if not field.endswith('s')]

    # 4) order the field and schema lists
        # order subgraph_query_field_list by alphabet values.
        sorted_subgraph_query_field_list = sorted(subgraph_query_field_list, key=lambda x: x.rstrip('s'))
        # order subgraph schema list by alphabet values. If '_' is first character, sort by the next strig index.
        sorted_subgraph_schema_query_list = sorted(subgraph_schema_query_list, key=lambda x: x.lstrip('_'))

        # PRINT HELP DEBUG STATEMENTS. CURRENTLY DISABLED
        print(f'subgraph_schema_query_list and subgraph_query_field_list (ordered)')
        for i in range(len(subgraph_query_field_list)):
            print(f'{sorted_subgraph_schema_query_list[i]}, {sorted_subgraph_query_field_list[i]}')
    
        # get values of endpoint after the last /
        subgraph_name = self.endpoint.split('/')[-1]

        outer_start = time.time()
        # automate querying subgraph data for each "queryable" subgraph schema object
        for i in range(len(sorted_subgraph_query_field_list)):
            # start query timer
            start = time.time()
            # get query field path
            field_list = self.getSchemaFields(self.subgraph, sorted_subgraph_schema_query_list[i])
            field_path = self.getFieldPath(self.subgraph, sorted_subgraph_query_field_list[i])
            # end query timer
            field_path_params = field_path(first=query_size) # params refers to the the GraphQL query search parameters such as first, last, descending, etc
            
            df = self.sub.query_df(field_path_params, field_list)
            
            # make a directory name of subgraph name and query field list. 
            # This will be used to create a directory to store the dataframes
            dir_name = f'{subgraph_name}'

            # make a directory to store the dataframes if directory doesn't exist
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)

            # save the dataframe to the directory
            df.to_csv(f'{dir_name}/{sorted_subgraph_query_field_list[i]}.csv')

            self.data_list.append(df)
            end = time.time()
            # PRINT DEBUG TO UNDERSTAND WHAT IS BEING QUERIED
            print(f'Round {i} - query time was {end - start: .3f} seconds \nschema {sorted_subgraph_schema_query_list[i]} with {sorted_subgraph_query_field_list[i]}')
            print(f'There are {len(field_list)} fields in the query - {field_list}. \nLength of df is {len(df)}.')
        outer_end = time.time()

        print(f'{subgraph_name} query took {outer_end - outer_start: .3f} seconds. Running total: {len(self.data_list)} schema dataframes and {sum([len(df) for df in self.data_list])} total rows retrieved.')
