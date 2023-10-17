from tdstone2.tdstone import TDStone
from tdstone2.tdscode import Code
from tdstone2.tdsmodel import Model
from tdstone2.tdsmapper import Mapper
from tdstone2.utils import execute_query,get_partition_datatype, get_sto_parameters
import os
import uuid
import json
import teradataml as tdml




class HyperModel():
    
    def __init__(self, tdstone, id = None, metadata ={},
                 script_path = None,
                 model_parameters = None,
                 dataset = None,
                 id_row = None,
                 id_partition = None,
                 id_fold = None,
                 fold_training = None
                ):
        
        self.id               = str(uuid.uuid4()) if id is None else id
        self.tdstone          = tdstone
        self.mapper_training  = None
        self.mapper_scoring   = None
        self.id_model         = None
        self.fold_training    = fold_training
        self.metadata = {'user': os.getlogin()}
        self.metadata.update(metadata)
        self.dataset          = dataset
        
        if script_path is not None and model_parameters is not None and dataset is not None and id_row is not None and id_partition is not None and fold_training is not None:
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
            self.mapper_training = Mapper(tdstone=self.tdstone,
                                          mapper_type  = 'training',
                                          id_row       = id_row,
                                          id_partition = id_partition,
                                          id_fold      = id_fold,
                                          dataset      = dataset
                                         )
            self.mapper_training.upload()
            self.mapper_training.fill_mapping_full(model_id=self.id_model)
            self.mapper_training.create_on_clause(fold=self.fold_training)
            self.mapper_training.create_sto_view()
            
            # create the mapper for model scoring
            self.mapper_scoring = Mapper(tdstone=self.tdstone,
                                         mapper_type  = 'scoring',
                                         id_row       = self.mapper_training.id_row,
                                         id_partition = self.mapper_training.id_partition,
                                         id_fold      = self.mapper_training.id_fold,
                                         dataset      = self.mapper_training.dataset,
                                         trained_model_repository = self.mapper_training.trained_model_repository
                                        )
            
            self.mapper_scoring.upload()
            self.mapper_scoring.create_on_clause()
            #self.mapper_scoring.create_sto_view()
            self.mapper_scoring.fill_mapping_full(model_id=self.id_model)
            self._register_hyper_model()
            print('hyper model :', self.id)

            
    @execute_query
    def _register_hyper_model(self):
        
        query = f"""
        INSERT INTO {self.tdstone.schema_name}.{self.tdstone.hyper_model_repository}
            (ID, ID_MODEL, ID_MAPPER_TRAINING, ID_MAPPER_SCORING, METADATA)
             VALUES
            ('{self.id}',
             '{self.id_model}',
             '{self.mapper_training.id}',
             '{self.mapper_scoring.id}',
             '{json.dumps(self.metadata).replace("'", '"')}');
        """
        print(f'register hyper model with id : {self.id}')
        return query
        
        
        
    def train(self, full_mapping_update = True):
        if full_mapping_update:
            self.mapper_training.fill_mapping_full(model_id=self.id_model)
        self.mapper_training.execute_mapper()       
        return
        
    def score(self, full_mapping_update = True):
        if full_mapping_update:
            self.mapper_scoring.fill_mapping_full(model_id=self.id_model)
        self.mapper_scoring.create_on_clause()
        self.mapper_scoring.execute_mapper()        
        return
    
    def get_trained_models(self):
        print(self.tdstone.schema_name, self.mapper_training.model_repository)
        return tdml.DataFrame(tdml.in_schema(self.tdstone.schema_name, self.mapper_training.trained_model_repository))
    
    def get_model_predictions(self):
        print(self.tdstone.schema_name, self.mapper_scoring.scores_repository)
        return tdml.DataFrame(tdml.in_schema(self.tdstone.schema_name, self.mapper_scoring.scores_repository))

    def download(self, id, tdstone=None):

        if tdstone is not None:
            self.tdstone = tdstone

        query = f"""
        SELECT 
           ID
        ,  ID_MODEL
        ,  ID_MAPPER_TRAINING
        ,  ID_MAPPER_SCORING
        ,  METADATA
        FROM {self.tdstone.schema_name}.{self.tdstone.hyper_model_repository}
        WHERE ID = '{id}'
        """

        df = tdml.DataFrame.from_query(query).to_pandas().reset_index()
        #print(df)
        if df.shape[0] > 0:
            self.id              = df.ID.values[0]
            self.id_model        = df.ID_MODEL.values[0]
            id_mapper_training   = df.ID_MAPPER_TRAINING.values[0]
            self.mapper_training = Mapper(tdstone=self.tdstone)
            self.mapper_training.download(id=id_mapper_training)
            id_mapper_scoring   = df.ID_MAPPER_SCORING.values[0]
            self.mapper_scoring = Mapper(tdstone=self.tdstone)
            self.mapper_scoring.download(id=id_mapper_scoring)
            self.metadata = eval(df.METADATA.values[0])
        else:
            print('there is no hyper model with this id')

    def retrieve_code_and_data(self, Partition=None, with_data=False):

        # Get the model_id from list_mapping:
        if Partition is None:
            df = self.mapper_training.list_mapping().to_pandas(num_rows=1)
            Partition = df.iloc[:, 1:-2]
            Partition = {c: v[0] for c, v in zip(Partition.columns, Partition.values.tolist())}
        else:
            df = self.mapper_training.list_mapping()
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
            df = tdml.DataFrame(self.mapper_training.dataset)
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
