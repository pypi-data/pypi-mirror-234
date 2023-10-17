from tdstone2.tdstone import TDStone
from tdstone2.tdscode import Code
from tdstone2.tdsmodel import Model
from tdstone2.tdsmapper import Mapper
from tdstone2.utils import execute_query, get_partition_datatype, get_sto_parameters
import os
import uuid
import json
import teradataml as tdml


class FeatureEngineering():

    def __init__(self, tdstone, id=None, metadata={},
                 script_path=None,
                 model_parameters=None,
                 dataset=None,
                 id_row=None,
                 id_partition=None,
                 feature_engineering_type=None
                 ):

        self.id              = str(uuid.uuid4()) if id is None else id
        self.tdstone         = tdstone
        self.mapper          = None
        self.id_model        = None
        self.metadata        = {'user': os.getlogin()}
        self.metadata.update(metadata)
        self.dataset         = dataset
        self.feature_engineering_type = feature_engineering_type

        if script_path is not None and model_parameters is not None and dataset is not None and id_row is not None and id_partition is not None and feature_engineering_type is not None:
            # register and upload the code
            mycode = Code(tdstone=self.tdstone)
            mycode.update_metadata(metadata)
            mycode.update_script(script_path)
            mycode.upload()

            arguments = {}
            arguments["sto_parameters"] = get_sto_parameters(tdml.DataFrame(self.dataset))
            arguments["model_parameters"] = model_parameters

            # register and upload the model
            model = Model(tdstone=self.tdstone)
            model.attach_code(mycode.id)
            model.update_arguments(arguments)
            model.update_metadata(metadata)
            model.upload()
            self.id_model = model.id

            # create the mapper for model training
            self.mapper = Mapper(tdstone      = self.tdstone,
                                 mapper_type  = self.feature_engineering_type,
                                 id_row       = id_row,
                                 id_partition = id_partition,
                                 dataset      = dataset
                                 )
            self.mapper.upload()
            self.mapper.fill_mapping_full(model_id=self.id_model)
            self.mapper.create_on_clause()
            self.mapper.create_sto_view()
            self._register_feature_engineering_model()

            print('feature engineering process :', self.id)

    @execute_query
    def _register_feature_engineering_model(self):

        query = f"""
        INSERT INTO {self.tdstone.schema_name}.{self.tdstone.feature_engineering_process_repository}
            (ID, ID_MODEL, ID_MAPPER, FEATURE_ENGINEERING_TYPE, METADATA)
             VALUES
            ('{self.id}',
             '{self.id_model}',
             '{self.mapper.id}',
             '{self.feature_engineering_type}',
             '{json.dumps(self.metadata).replace("'", '"')}');
        """
        print(f'register feature engineering model with id : {self.id}')
        return query

    def transform(self, full_mapping_update=True):
        if full_mapping_update:
            self.mapper.fill_mapping_full(model_id=self.id_model)
        self.mapper.execute_mapper()
        return

    def get_computed_features(self):
        if self.feature_engineering_type == 'feature engineering':
            print(self.tdstone.schema_name, self.mapper.features_repository)
            return tdml.DataFrame(tdml.in_schema(self.tdstone.schema_name, self.mapper.features_repository))
        elif self.feature_engineering_type == 'feature engineering reducer':
            print(self.tdstone.schema_name, self.mapper.reduced_feature_repository)
            return tdml.DataFrame(tdml.in_schema(self.tdstone.schema_name, self.mapper.reduced_feature_repository))

    def download(self, id, tdstone=None):

        if tdstone is not None:
            self.tdstone = tdstone

        query = f"""
        SELECT 
           ID
        ,  ID_MODEL
        ,  ID_MAPPER
        ,  FEATURE_ENGINEERING_TYPE
        ,  METADATA
        FROM {self.tdstone.schema_name}.{self.tdstone.feature_engineering_process_repository}
        WHERE ID = '{id}'
        """

        df = tdml.DataFrame.from_query(query).to_pandas().reset_index()
        # print(df)
        if df.shape[0] > 0:
            self.id = df.ID.values[0]
            self.id_model = df.ID_MODEL.values[0]
            id_mapper = df.ID_MAPPER.values[0]
            self.mapper = Mapper(tdstone=self.tdstone)
            self.mapper.download(id=id_mapper, tdstone=self.tdstone)
            self.metadata = eval(df.METADATA.values[0])
            self.feature_engineering_type = df.FEATURE_ENGINEERING_TYPE.values[0]
        else:
            print('there is no feature engineering process with this id')

    def retrieve_code_and_data(self, Partition=None, with_data=False):

        # Get the model_id from list_mapping:
        if Partition is None:
            df = self.mapper.list_mapping().to_pandas(num_rows=1)
            Partition = df.iloc[:, 1:-2]
            Partition = {c: v[0] for c, v in zip(Partition.columns, Partition.values.tolist())}
        else:
            df = self.mapper.list_mapping()
            df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)
            where = " and ".join(
                [k + "='" + v + "'" if type(v) == str else k + "=" + str(v) for k, v in Partition.items()])
            df = tdml.DataFrame.from_query(f"""
                SEL *
                FROM {df._table_name}
                WHERE {where}
            """).to_pandas(num_rows=1)

        id_model = df.ID_MODEL.values[0]

        # Get the Code and the Arguments
        df = self.tdstone.list_models()
        df = df[df.ID == id_model].to_pandas(num_rows=1)
        arguments = eval(df.ARGUMENTS.values[0])
        id_code = df.ID_CODE.values[0]

        # Get the Code
        df = self.tdstone.list_codes(with_full_script=True)
        df = df[df.ID == id_code].to_pandas(num_rows=1)
        code = df.CODE.values[0].decode()

        results = {}
        results['code'] = code
        results['arguments'] = arguments['model_parameters']

        if with_data:
            df = tdml.DataFrame(self.mapper.dataset)
            df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)
            where = " and ".join(
                [k + "='" + v + "'" if type(v) == str else k + "=" + str(v) for k, v in Partition.items()])
            df = tdml.DataFrame.from_query(f"""
                SEL *
                FROM {df._table_name}
                WHERE {where}
            """).to_pandas().reset_index()
            results['data'] = df

        return results
