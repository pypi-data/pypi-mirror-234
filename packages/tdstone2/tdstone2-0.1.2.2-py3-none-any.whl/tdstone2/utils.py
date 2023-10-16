import functools
import teradataml as tdml
import os
import re
import plotly.graph_objects as go

from packaging import version

def get_connection_username():
    return str(tdml.get_context().url).split('USER=')[1]

def is_version_greater_than(tested_version, base_version="17.20.00.03"):
    """
    Check if the tested version is greater than the base version.

    Args:
        tested_version (str): Version number to be tested.
        base_version (str, optional): Base version number to compare. Defaults to "17.20.00.03".

    Returns:
        bool: True if tested version is greater, False otherwise.
    """
    return version.parse(tested_version) > version.parse(base_version)

def execute_query(f):
    """
    Decorator to execute a query. It wraps around the function and adds exception handling.

    Args:
        f (function): Function to be decorated.

    Returns:
        function: Decorated function.
    """
    @functools.wraps(f)
    def wrapped_f(*args, **kwargs):
        query = f(*args, **kwargs)
        if is_version_greater_than(tdml.__version__, base_version="17.20.00.03"):
            if type(query) == list:
                for q in query:
                    try:
                        tdml.execute_sql(q)
                    except Exception as e:
                        print(str(e).split('\n')[0])
                        print(q)
            else:
                try:
                    tdml.execute_sql(query)
                except Exception as e:
                    print(str(e).split('\n')[0])
                    print(query)
        else:
            if type(query) == list:
                for q in query:
                    try:
                        tdml.get_context().execute(q)
                    except Exception as e:
                        print(str(e).split('\n')[0])
                        print(q)
            else:
                try:
                    tdml.get_context().execute(query)
                except Exception as e:
                    print(str(e).split('\n')[0])       
                    print(query)
        return 
    return wrapped_f

def execute_query_with_path(f):
    """
    Decorator to execute a query with a specified path.
    It wraps around the function, executes the query, and then removes the file.

    Args:
        f (function): Function to be decorated.

    Returns:
        function: Decorated function.
    """
    @functools.wraps(f)
    def wrapped_f(*args, **kwargs):
        query, path = f(*args, **kwargs)
        #print(path)
        if is_version_greater_than(tdml.__version__, base_version="17.20.00.03"):
            tdml.execute_sql(query,[[path]])
        else:
            tdml.get_context().execute(query, path)
        
    return wrapped_f


def get_partition_datatype(tddf, columns):
    """
    Fetches the data types of specified columns in a Teradata DataFrame (tddf).

    The function queries the data type of each column specified and returns it as a dictionary.

    :param tddf: Teradata DataFrame
        Input DataFrame for which data types are to be fetched.

    :param columns: list
        List of column names for which data types need to be retrieved.

    :return: dict
        Dictionary where keys are column names and values are the data types of the respective columns.

    :Note: The function assumes the use of Teradata and Teradata ML (tdml) for data manipulation and querying.
    """

    # Try to get the table name from the tddf
    try:
        table_name = tddf._table_name
    except Exception as e:
        # If the table name attribute is not present, execute the tddf to get it
        tddf = tddf._DataFrame__execute_node_and_set_table_name(tddf._nodeid, tddf._metaexpr)
        table_name = tddf._table_name

    # Construct the SQL query to get the datatype of each column
    query = f"""
    SELECT TOP 1
        {','.join(['TYPE(' + x + ') AS ' + x for x in columns])}
    FROM {table_name}
    """

    # Execute the SQL query and convert the result to a pandas DataFrame
    df = tdml.DataFrame.from_query(query).to_pandas()

    # Construct a dictionary of column names and their data types
    types = {}
    for c in df.columns:
        types[c] = df[c].values[0].strip()

    return types


def get_sto_parameters(dataset):
    """
    Generate a dictionary of parameters related to the dataset, particularly focusing on column types.

    The function identifies columns of type float, integer, and also provides an output format.

    :param dataset: pd.DataFrame
        Input dataset for which the parameters are being generated.

    :return: dict
        Dictionary containing the following keys:
        - columnnames: All column names of the dataset.
        - float_columnames: Column names with float data type.
        - integer_columnames: Column names with integer data type.
        - category_columns: An empty list (reserved for potential future use).
        - output_format: Format for output, default is ['pickle'].

    :Note: The function depends on another function `get_partition_datatype` which is not provided in this context.
    """

    # Get the data types of each partition of the dataset using an external function
    types = get_partition_datatype(dataset, dataset.columns)

    sto_parameters = {}  # Initialize an empty dictionary for the parameters

    # Assign all column names
    sto_parameters["columnnames"] = list(dataset.columns)

    # Identify and assign float column names
    sto_parameters["float_columnames"] = [k for k, v in types.items() if v.lower() == 'float']

    # Identify and assign integer column names
    sto_parameters["integer_columnames"] = [k for k, v in types.items() if 'int' in v.lower()]

    # Placeholder for category columns, currently an empty list
    sto_parameters["category_columns"] = []

    # Assign the default output format
    sto_parameters['output_format'] = ['pickle']

    return sto_parameters


def cleanup(schema, rootname='TDS_'):
    """
    Clean up tables and views in the specified schema that have names starting with the given rootname.

    For tables or views starting with the given rootname (default "TDS_"), the function will attempt to drop them.
    The function can handle different versions of the 'tdml' module, using different methods for table and view
    deletion based on the module version.

    :param schema: str
        The name of the schema from which tables and views will be deleted.

    :param rootname: str, optional
        The prefix for table and view names to target for deletion. Default is "TDS_".

    :return: None
    """

    # Iterate over tables in the provided schema
    for x in tdml.db_list_tables(schema_name=schema).TableName.tolist():

        # Only process tables or views starting with the rootname
        if x.startswith(rootname):
            try:
                # If the 'tdml' module version is greater than the specified base version, use the new method for table deletion
                if is_version_greater_than(tdml.__version__, base_version="17.20.00.03"):
                    tdml.execute_sql(f"DROP TABLE {schema}.{x}")
                else:
                    # For older 'tdml' module versions, use the old method for table deletion
                    tdml.get_connection().execute(f"DROP TABLE {schema}.{x}")

                # Output the action taken
                print(f"DROP TABLE {schema}.{x}")

            except Exception as e:
                # If dropping a table fails, attempt to drop a view
                try:
                    # If the 'tdml' module version is greater than the specified base version, use the new method for view deletion
                    if is_version_greater_than(tdml.__version__, base_version="17.20.00.03"):
                        tdml.execute_sql(f"DROP VIEW {schema}.{x}")
                    else:
                        # For older 'tdml' module versions, use the old method for view deletion
                        tdml.get_connection().execute(f"DROP VIEW {schema}.{x}")

                    # Output the action taken
                    print(f"DROP VIEW {schema}.{x}")

                except Exception as e:
                    # If both table and view deletions fail, print the error message
                    print(x, str(e).split('\n')[0])


def _analyze_sql_query(sql_query):
    """
    Analyze a SQL query to extract the source tables, target tables, and views.

    The function uses regular expressions to search for patterns indicative
    of source tables, target tables, and views in the given SQL query.

    :param sql_query: str
        A string containing a SQL query to be analyzed.

    :return: dict
        A dictionary containing lists of source tables, target tables, and views.
        Format: {
            'source': [source_tables],
            'target': [target_tables]
        }
    """

    # Regular expression patterns for different SQL components
    create_table_pattern = r'CREATE\s+TABLE\s+([\w\s\.\"]+?)\s+AS'
    insert_into_pattern = r'INSERT\s+INTO\s+([\w\s\.\"]+?)'
    create_view_pattern = r'(CREATE|REPLACE)\s+VIEW\s+([\w\s\.\"]+?)\s+AS'
    select_pattern = r'(FROM|JOIN)\s+([\w\s\.\"]+?)(?=\s*(,|on|group|$|where))'

    # Find all matches in the SQL query for each pattern
    create_table_matches = re.findall(create_table_pattern, sql_query, re.IGNORECASE)
    insert_into_matches = re.findall(insert_into_pattern, sql_query, re.IGNORECASE)
    create_view_matches = re.findall(create_view_pattern, sql_query, re.IGNORECASE)
    select_matches = re.findall(select_pattern, sql_query, re.IGNORECASE)

    # Extract the actual table or view name from the match tuples
    create_table_matches = [match[0] if match[0] else match[1] for match in create_table_matches]
    insert_into_matches = [match[0] if match[0] else match[1] for match in insert_into_matches]
    create_view_matches = [match[1] if match[0] else match[1] for match in create_view_matches]
    select_matches = [match[1] for match in select_matches]

    table_names = {
        'source': [],
        'target': []
    }

    # Categorize the matched tables and views into 'source' or 'target'
    table_names['target'].extend(create_table_matches)
    table_names['target'].extend(insert_into_matches)
    table_names['target'].extend(create_view_matches)
    table_names['source'].extend(select_matches)

    # Remove duplicate table and view names
    table_names['source'] = list(set(table_names['source']))
    table_names['target'] = list(set(table_names['target']))

    return table_names


def analyze_sql_query(sql_query, df=None, target=None, root_name='ml__'):
    """
    Analyzes the provided SQL query to determine source and target tables/views relationships.
    It then captures these relationships in a pandas DataFrame.

    :param sql_query: str
        A string containing the SQL query to be analyzed.
    :param df: pd.DataFrame, optional
        An existing DataFrame to append the relationships to. If not provided, a new DataFrame is created.
    :param target: str, optional
        Name of the target table/view. If not provided, it's deduced from the SQL query.

    :return: pd.DataFrame
        A DataFrame with two columns: 'source' and 'target', representing the relationships.

    :Note: This function is specifically tailored for Teradata and makes use of teradataml (tdml) for certain operations.
    """

    # Extract source and potential target tables/views from the provided SQL query
    table_name = _analyze_sql_query(sql_query)

    # If df is not provided, initialize it; else append to the existing df
    table_name['target'] = [target] * len(table_name['source'])
    if df is None:
        df = pd.DataFrame(table_name)
    else:
        df = pd.concat([df, pd.DataFrame(table_name)], ignore_index=True)

    # Check for teradataml views in the source and recursively analyze them
    for obj in table_name['source']:
        if root_name in obj:
            # It's a teradataml view. Fetch its definition.
            sql_query_ = tdml.execute_sql(f"SHOW VIEW {obj}").fetchall()[0][0]

            # Recursively analyze the view definition to get its relationships
            df = analyze_sql_query(sql_query_, df, target=obj)

    return df


def plot_graph(df):
    """
    Visualizes a given dataframe's source-target relationships using a Sankey diagram.

    :param df: pd.DataFrame
        The input dataframe should have two columns: 'source' and 'target'.
        Each row represents a relationship between a source and a target.

    :Note: This function makes use of Plotly's Sankey diagram representation for visualization.

    :return: None
        The function outputs the Sankey diagram and doesn't return anything.
    """

    # Create a list of unique labels combining sources and targets from the dataframe
    labels = list(pd.concat([df['source'], df['target']]).unique())

    # Convert source and target names to indices based on their position in the labels list
    source_indices = df['source'].apply(lambda x: labels.index(x))
    target_indices = df['target'].apply(lambda x: labels.index(x))

    # Construct the Sankey diagram with nodes (sources & targets) and links (relationships)
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,  # Space between the nodes
            thickness=20,  # Node thickness
            line=dict(color="black", width=0.5),  # Node border properties
            label=labels,  # Labels for nodes
            color="blue"  # Node color
        ),
        link=dict(
            source=source_indices,  # Link sources
            target=target_indices,  # Link targets
            value=[1] * len(df)  # Assuming equal "flow" for each link. Can be modified if needed.
        )
    )])

    # Customize the layout, such as setting the title and font size
    fig.update_layout(title_text="Hierarchical Data Visualization", font_size=10)

    # Display the Sankey diagram
    fig.show()

def materialize_view(tddf, view_name, schema_name):
    """
    Materializes a given teradataml DataFrame as a view in the database with sub-views, if needed. This function
    helps in creating nested views, where complex views are broken down into simpler sub-views to simplify debugging
    and optimization. Each sub-view is named based on the main view's name with an additional suffix.

    Parameters:
    :param tddf: teradataml.DataFrame
        The teradataml dataframe whose view needs to be materialized.
    :param view_name: str
        The name of the main view to be created.
    :param schema_name: str
        The schema in which the view should be created.

    Returns:
    :return: teradataml.DataFrame
        A teradataml DataFrame representation of the created view.

    Notes:
    This function is specific to the teradataml library, and assumes the existence of certain attributes in the input DataFrame.
    """

    # Create the _table_name attribute for the teradataml DataFrame if it doesn't exist
    tddf._DataFrame__execute_node_and_set_table_name(tddf._nodeid, tddf._metaexpr)

    # Generate the dependency graph for the input DataFrame's SQL representation
    tddf_graph = analyze_sql_query(tddf.show_query(), target=tddf._table_name)

    # Extract only the target nodes from the graph, excluding the main table/view
    nodes = list(set(tddf_graph['target']) - set([tddf._table_name]))

    # Generate new names for sub-views based on the main view's name and store in a mapping dictionary
    mapping = {n: schema_name + '.' + view_name + '_sub_' + str(i) for i, n in enumerate(nodes)}

    # Replace or create the sub-views with their new names in the database
    for old_name, new_name in mapping.items():
        query = tdml.execute_sql(f"SHOW VIEW {old_name}").fetchall()[0][0].lower()
        query = query.replace('create', 'replace')
        for old_sub_name, new_sub_name in mapping.items():
            query = query.replace(old_sub_name, new_sub_name)
        tdml.execute_sql(query)

    # Construct the final view by replacing the old names with new ones in the SQL representation
    mapping[tddf._table_name] = view_name
    query = tddf.show_query().lower()
    query = f'replace view {schema_name}.{view_name} AS \n' + query
    for old_name, new_name in mapping.items():
        query = query.replace(old_name, new_name)

    # Execute the final query to create the main view
    tdml.execute_sql(query)

    # Return a teradataml DataFrame representation of the created view
    return tdml.DataFrame(tdml.in_schema(schema_name, view_name))
