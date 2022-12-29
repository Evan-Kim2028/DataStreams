import pandas as pd
import os
import time

from dataclasses import dataclass
from subgrounds.subgraph.subgraph import Subgraph
from subgrounds.schema import TypeRef
from subgrounds.subgrounds import Subgrounds
from subgrounds.subgraph.fieldpath import FieldPath
from subgrounds.subgraph import SyntheticField

# pd.set_option('display.max_columns', None)
# pd.set_option('display.expand_frame_repr', False)
# pd.set_option('max_colwidth', None)

@dataclass
class Streamer:
    '''
    Wrapper/Helper class built ontop of Subgrounds that allows user to easily access the subgraph schema and query the subgraph for all possible queries.

    # There are three components for the Subgrounds pipeline:
    # 1) Load Subgrounds - The main entry point for the pipeline, Subgrounds is used to query the subgraph and load the data into dataframes.
    # 2) Load Subgraph -  Load the schema data from a graphql endpoint. Specifically the schema data pertaining to `Query`. 
    # 3) Define Query Path - The query path is defined automatically to run every possible query on the subgraph and returns a list of dataframes.
    '''
    sub: Subgrounds
    endpoint: str
    subgraph: Subgraph
    # TODO - turn this into a dictionary with respective query field name for easier lookup. THis would be a nice to have, but the names are also saved in the directory too already so not sure this is necessary.
    data_list = []

    def runStreamer(self):
        '''
        Use runStreamer() get all queryable fields from a subgraph. Streamer will run every possible query on the subgraph and return a list of dataframes.
        '''
    # 1) get schema list 
        schema_list = self.getSubgraphSchema(self.subgraph)
    # 2) get schema query field list
        query_field_list = self.getSchemaFields(self.subgraph, schema_list[schema_list.index('Query')])

    # 3) get field paths from 2
    # 4) filter, format, and sort. End result is subgraph_query_field_list -> sorted_subgraph_field_query_list steps
        filtered_schema_list = [x for x in schema_list if not x.endswith('_') and x != 'Query' and x != 'Subscription']
        # format query fields
        fmt_query_field_list = [self.formatFieldStr(field) for field in query_field_list]
        # drop empty values if there are any. Empty fields will break the query.
        fmt_query_field_list = [field for field in fmt_query_field_list if field != '']
        # make a query field list with queryable fields - these are plural values that end with 's'.
        subgraph_query_field_list = [field for field in fmt_query_field_list if field.endswith('s')]
        # make a subgraph schema list with schema objects that relate to the query fields. These are singular values that do not end with 's'.
        subgraph_schema_query_list = [field[0].upper() + field[1:] for field in filtered_schema_list if not field.endswith('s')]

    # 4b) order the field and schema lists
        # order subgraph_query_field_list by alphabet values.
        sorted_subgraph_query_field_list = sorted(subgraph_query_field_list, key=lambda x: x.rstrip('s'))
        # order subgraph schema list by alphabet values. If '_' is first character, sort by the next strig index.
        sorted_subgraph_schema_query_list = sorted(subgraph_schema_query_list, key=lambda x: x.lstrip('_'))

        # PRINT HELP DEBUG STATEMENTS. CURRENTLY DISABLED
        # print(f'subgraph_schema_query_list and subgraph_query_field_list (ordered)')
        # for i in range(len(subgraph_query_field_list)):
        #     print(f'{sorted_subgraph_schema_query_list[i]}, {sorted_subgraph_query_field_list[i]}')
    
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
            field_path_params = field_path(first=5)
            
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
            # print(f'Round {i} - query time was {end - start: .3f} seconds \nschema {sorted_subgraph_schema_query_list[i]} with {sorted_subgraph_query_field_list[i]}')
            # print(f'There are {len(field_list)} fields in the query - {field_list}. \nLength of df is {len(df)}.')
        outer_end = time.time()
        print(f'{subgraph_name} query took {outer_end - outer_start: .3f} seconds. Running total: {len(self.data_list)} schema dataframes and {sum([len(df) for df in self.data_list])} total rows retrieved.')


    def getFieldPath(self, subgraph: Subgraph, field: str,  operation: str ='Query') -> FieldPath:
        '''
        Use getFieldPath to get a FieldPath from a string.

        Args:
            subgraph (Subgraph) = Subgraph object with a loaded graphql endpoint
            field (str) = Enter the string that will be converted to a FieldPath
            operation (str) = Enter one of the following - 'Query', 'Mutation', or 'Subscription'. Default is 'Query' because that is most commonly used.
        Returns:
            FieldPath = FieldPath object
        '''
        return subgraph.__getattribute__(operation).__getattribute__(field)

    def getSubgraphSchema(self, subgraph: Subgraph) -> list[str]:
        '''
        Use getSubgraphSchema to fetch a schema list from a subgraph object.

        Args:
            subgraph (Subgraph) = Subgraph object with a loaded graphql endpoint
        Returns:
            list[str] = schema objects list from subgraph
        '''
        return list(name for name, type_ in subgraph._schema.type_map.items() if type_.is_object)

    def getSchemaFields(self, subgraph: Subgraph, schema_object: str) -> list[str]:
        '''
        Use getSubgraphField to get a list of SchemaFields from a subgraph.

        Args:
            subgraph (Subgraph) = Subgraph object with a loaded graphql endpoint
            schema_object (str) = Enter the schama object string that you want to get all fields for
        Returns:
            list[str] = list of field strings from schema_object
        '''
        return list(field.name for field in subgraph.__getattribute__(schema_object)._object.fields)

    def formatFieldStr(self, field: str) -> str:
        # if value does not end with a s and does not start and end with _, make the first non _ character in the string a capital letter
        '''
        Use formatFieldStr to format the field string to be queryable. In order to make the field string queryable, the first non _ character must be capitalized.

        Args:
            field (str) = field string
        Returns:
            str = formatted field string
        '''
        if not field.endswith('s') and not field.startswith('_'):
            field = field[0].upper() + field[1:]
        return field