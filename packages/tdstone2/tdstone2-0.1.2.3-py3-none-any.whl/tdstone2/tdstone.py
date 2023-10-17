from tdstone2.utils import execute_query
import teradataml as tdml
from tqdm import tqdm
import os

file_list = ['tds_feature_engineering','tds_feature_engineering_reducer','tds_training','tds_scoring','tds_feature_engineering_jsonoutput']
this_dir, this_filename = os.path.split(__file__)

class TDStone():
    """
    Class to manage the TDStone system.
    """
    def __init__(self, schema_name, **kwargs):
        """
        Initialize the TDStone object.
        ...
        """        
        self.schema_name      = schema_name
        self.SEARCHUIFDBPATH  = kwargs.get('SEARCHUIFDBPATH', schema_name)
        self.code_repository  = kwargs.get('code_repository', 'TDS_CODE_REPOSITORY')
        self.model_repository = kwargs.get('model_repository', 'TDS_MODEL_REPOSITORY')
        self.trained_model_repository = kwargs.get('trained_model_repository', 'TDS_TRAINED_MODEL_REPOSITORY')
        self.mapper_repository = kwargs.get('mapper_repository', 'TDS_MAPPER_REPOSITORY')
        self.hyper_model_repository = kwargs.get('hyper_model_repository', 'TDS_HYPER_MODEL_REPOSITORY')
        self.feature_engineering_process_repository = kwargs.get('feature_engineering_process_repository', 'TDS_FEATURE_ENGINEERING_PROCESS_REPOSITORY')
        
    @execute_query
    def PushFile(self):
        """
        This method is used to create a list of database queries that will update 
        the search path, remove the current file, and then install a new file based 
        on the operating system type. It is specifically designed for handling file 
        management on different systems.

        Returns:
            list: A list of SQL queries to be executed.
        """

        # Creating an empty list to hold the queries
        queries = []

        # Appending the SET SESSION and DATABASE queries to the list
        queries.append('SET SESSION SEARCHUIFDBPATH = "{}"'.format(self.SEARCHUIFDBPATH))
        queries.append('DATABASE {}'.format(self.SEARCHUIFDBPATH))

        # Looping through each filename in the file list
        for filename in (pbar := tqdm(file_list)):
            pbar.set_description(f"Installing {filename}")
            # Adding a command to remove the existing file
            queries.append("CALL SYSUIF.REMOVE_FILE('{}',1);".format(filename))

            # Checking the OS name to determine the file path format
            if os.name == 'nt':
                # If it's Windows, we need to format the path a little differently
                queries.append("CALL SYSUIF.INSTALL_FILE('{}','{}','cz!{}')".format(filename,
                     filename+'.py',
                     os.path.join(this_dir, "data", filename+".py").replace("\\", "/").split(':')[1]))

            else:
                # If it's Linux or another OS, we can use the standard path format
                queries.append("CALL SYSUIF.INSTALL_FILE('{}','{}','cz!{}')".format(filename,
                     filename+'.py',
                     os.path.join(this_dir, "data", filename+".py")))

        # Return the complete list of queries
        return queries

    def setup(self, install_files=True):
        self._create_code_repository()
        self._create_model_repository()
        self._create_mapper_repository()
        self._create_hypermodel_repository()
        self._create_feature_engineering_process_repository()
        if install_files:
            self.PushFile()
####################################################################################################
#
#               CCCCC   OOOOO  DDDDD   EEEEEEE 
#              CC    C OO   OO DD  DD  EE      
#              CC      OO   OO DD   DD EEEEE   
#              CC    C OO   OO DD   DD EE      
#               CCCCC   OOOO0  DDDDDD  EEEEEEE 
#
####################################################################################################  

    @execute_query
    def _create_code_repository(self):
        """
        Create a code repository in the TDStone system.

        Returns:
            query: SQL query to create the code repository.
        """        
        query = f"""
            CREATE MULTISET TABLE {self.schema_name}.{self.code_repository},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                ID VARCHAR(36) NOT NULL,
                CODE_TYPE VARCHAR(255) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL,
                CODE BLOB,
                METADATA JSON(32000), 
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME	
            )
            PRIMARY INDEX (ID);
        """
        return query
    
    def list_codes(self, with_full_script = False, current_only = True):
        """
        List the code in the TDStone system.

        Args:
            with_full_script (bool, optional): If True, the full script is listed. Defaults to False.
            current_only (bool, optional): If True, only the current version is listed. Defaults to True.

        Returns:
            DataFrame: A DataFrame with the code details.
        """        
        if current_only:
            query = "CURRENT VALIDTIME \n"
        else:
            query = ''
            
        query = query + 'SELECT \n'
        
        if with_full_script:
            query = query + '* \n'
        else:
            if current_only:
                query = query + ',\n'.join(['ID','CODE_TYPE','METADATA'])
            else:
                query = query + ',\n'.join(['ID','CODE_TYPE','METADATA','ValidStart','ValidEnd'])
                
        query = query + f'\n FROM {self.schema_name}.{self.code_repository}'
        
        return tdml.DataFrame.from_query(query)
    
    @execute_query
    def remove_codes(self, code_id):
        """
        Remove a code from the TDStone system.

        Args:
            code_id (str or list): The ID or list of IDs of the code to be removed.

        Returns:
            query: SQL query to remove the code.
        """        
        if type(code_id) == list:
            code_list = ",".join(["'"+x+"'" for x in code_id])
            query = f"""
                DELETE {self.schema_name}.{self.code_repository} WHERE ID IN ({code_list});
                """
        else:
            query = f"""
                DELETE {self.schema_name}.{self.code_repository} WHERE ID = '{code_id}';
                """
        
        return query

####################################################################################################
#
#              MM    MM  OOOOO  DDDDD   EEEEEEE LL      
#              MMM  MMM OO   OO DD  DD  EE      LL      
#              MM MM MM OO   OO DD   DD EEEEE   LL      
#              MM    MM OO   OO DD   DD EE      LL      
#              MM    MM  OOOO0  DDDDDD  EEEEEEE LLLLLLL 
#
####################################################################################################    
    @execute_query
    def _create_model_repository(self):
        """
        Create a model repository in the TDStone system.

        Returns:
            query: SQL query to create the model repository.
        """        
        query = f"""
        CREATE MULTISET TABLE {self.schema_name}.{self.model_repository},
        FALLBACK,
        NO BEFORE JOURNAL,
        NO AFTER JOURNAL,
        CHECKSUM = DEFAULT,
        DEFAULT MERGEBLOCKRATIO,
        MAP = TD_MAP1
        (
            ID VARCHAR(36) NOT NULL,
            ID_CODE VARCHAR(36),
            ARGUMENTS VARCHAR(32000) CHARACTER SET UNICODE NOT CASESPECIFIC NOT NULL, --JSON(32000),
            METADATA JSON(32000), 
            ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
            ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
            PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME	
        )
        PRIMARY INDEX (ID_CODE);
        """
        return query
    
    def list_models(self, current_only = True):
        """
        List the models in the TDStone system.

        Args:
            with_full_script (bool, optional): If True, the full script is listed. Defaults to False.
            current_only (bool, optional): If True, only the current version is listed. Defaults to True.

        Returns:
            DataFrame: A DataFrame with the model details.
        """        
        if current_only:
            query = "CURRENT VALIDTIME \n"
        else:
            query = ''
            
        query = query + 'SELECT \n'
        
        if current_only:
            query = query + ',\n'.join(['ID','ID_CODE','ARGUMENTS','METADATA'])
        else:
            query = query + ',\n'.join(['ID','ID_CODE','ARGUMENTS','METADATA','ValidStart','ValidEnd'])
                
        query = query + f'\n FROM {self.schema_name}.{self.model_repository}'
        
        return tdml.DataFrame.from_query(query)
    
    @execute_query
    def remove_models(self, model_id):
        """
        Remove a model from the TDStone system.

        Args:
            model_id (str or list): The ID or list of IDs of the model to be removed.

        Returns:
            query: SQL query to remove the model.
        """        
        if type(model_id) == list:
            model_list = ",".join(["'"+x+"'" for x in model_id])
            query = f"""
                DELETE {self.schema_name}.{self.model_repository} WHERE ID IN ({model_list});
                """
        else:
            query = f"""
                DELETE {self.schema_name}.{self.model_repository} WHERE ID = '{model_id}';
                """
        
        return query  
    
####################################################################################################
#
#              MM    MM   AAA   PPPPPP  PPPPPP  EEEEEEE RRRRRR  
#              MMM  MMM  AAAAA  PP   PP PP   PP EE      RR   RR 
#              MM MM MM AA   AA PPPPPP  PPPPPP  EEEEE   RRRRRR  
#              MM    MM AAAAAAA PP      PP      EE      RR  RR  
#              MM    MM AA   AA PP      PP      EEEEEEE RR   RR 
#
####################################################################################################

                                                   
    @execute_query
    def _create_mapper_repository(self):
        """
        Create a mapper repository in the TDStone system.

        Returns:
            query: SQL query to create the mapper repository.
        """        
        query = f"""
            CREATE MULTISET TABLE {self.schema_name}.{self.mapper_repository},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                ID VARCHAR(36) NOT NULL,
                MAPPER_TYPE VARCHAR(255) CHARACTER SET UNICODE,
                TABLE_NAME VARCHAR(255) CHARACTER SET UNICODE,
                CODE_REPOSITORY VARCHAR(255) CHARACTER SET UNICODE,
                MODEL_REPOSITORY VARCHAR(255) CHARACTER SET UNICODE,
                TRAINED_MODEL_REPOSITORY VARCHAR(255) CHARACTER SET UNICODE,
                FEATURE_REPOSITORY VARCHAR(255) CHARACTER SET UNICODE,
                SCORES_REPOSITORY VARCHAR(255) CHARACTER SET UNICODE,
                DATASET_OBJECT VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC,
                COL_ID_ROW VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC,
                COL_ID_PARTITION VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC,
                COL_FOLD VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC,
                ON_CLAUSE_VIEW VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC,
                STO_VIEW VARCHAR(2000) CHARACTER SET UNICODE NOT CASESPECIFIC,
                METADATA JSON(32000),
                ValidStart TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                ValidEnd TIMESTAMP(0) WITH TIME ZONE NOT NULL,
                PERIOD FOR ValidPeriod  (ValidStart, ValidEnd) AS VALIDTIME            
            )
            PRIMARY INDEX (ID);
            """
        return query
    
    def list_mappers(self, current_only = True, mapper_type = None):
        """
        List the mappers in the TDStone system.

        Args:
            with_full_script (bool, optional): If True, the full script is listed. Defaults to False.
            current_only (bool, optional): If True, only the current version is listed. Defaults to True.

        Returns:
            DataFrame: A DataFrame with the model details.
        """        
        if current_only:
            query = "CURRENT VALIDTIME \n"
        else:
            query = ''
            
        query = query + 'SELECT * \n'
        
               
        query = query + f'\n FROM {self.schema_name}.{self.mapper_repository}'
        
        if mapper_type is not None:
            query = query + f"\n WHERE MAPPER_TYPE = '{mapper_type}'"
        
        return tdml.DataFrame.from_query(query)
    
    @execute_query
    def remove_mappers(self, mapper_id):
        """
        Remove a model from the TDStone system.

        Args:
            model_id (str or list): The ID or list of IDs of the mapper to be removed.

        Returns:
            query: SQL query to remove the model.
        """        
        if type(mapper_id) == list and len(mapper_id)>0:
            mapper_list = ",".join(["'"+x+"'" for x in mapper_id])
            query = f"""
                DELETE {self.schema_name}.{self.mapper_repository} WHERE ID IN ({mapper_list});
                """
        else:
            query = f"""
                DELETE {self.schema_name}.{self.mapper_repository} WHERE ID = '{mapper_id}';
                """
        
        return query  
    
####################################################################################################
#
#              #HYPER MODEL 
#
####################################################################################################

                                                   
    @execute_query
    def _create_hypermodel_repository(self):
        """
        Create a mapper repository in the TDStone system.

        Returns:
            query: SQL query to create the mapper repository.
        """        
        query = f"""
            CREATE MULTISET TABLE {self.schema_name}.{self.hyper_model_repository},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                CREATION_DATE TIMESTAMP(6) WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
                ID VARCHAR(36) NOT NULL,
                ID_MODEL VARCHAR(36) NOT NULL,
                ID_MAPPER_TRAINING VARCHAR(36) NOT NULL,
                ID_MAPPER_SCORING VARCHAR(36) NOT NULL,
                METADATA JSON(32000)
            )
            PRIMARY INDEX (ID);
            """
        return query
    
    def list_hyper_models(self):
        """
        List the hyper models in the TDStone system.

        Returns:
            DataFrame: A DataFrame with the hyper model details.
        """        
            
        query = 'SELECT * \n'
        
               
        query = query + f'\n FROM {self.schema_name}.{self.hyper_model_repository}'
        
        
        return tdml.DataFrame.from_query(query)
    
    @execute_query
    def remove_hyper_models(self, hyper_model_id):
        """
        Remove a hyper model from the TDStone system.

        Args:
            model_id (str or list): The ID or list of IDs of the mapper to be removed.

        Returns:
            query: SQL query to remove the model.
        """        
        if type(hyper_model_id) == list and len(hyper_model_id)>0:
            hyper_model_list = ",".join(["'"+x+"'" for x in hyper_model_id])
            query = f"""
                DELETE {self.schema_name}.{self.hyper_model_repository} WHERE ID IN ({hyper_model_list});
                """
        else:
            query = f"""
                DELETE {self.schema_name}.{self.hyper_model_repository} WHERE ID = '{hyper_model_id}';
                """
        
        return query

    ####################################################################################################
    #
    #              #FEATURE ENGINEERING
    #
    ####################################################################################################

    @execute_query
    def _create_feature_engineering_process_repository(self):
        """
        Create a mapper repository in the TDStone system.

        Returns:
            query: SQL query to create the mapper repository.
        """
        query = f"""
            CREATE MULTISET TABLE {self.schema_name}.{self.feature_engineering_process_repository},
            FALLBACK,
            NO BEFORE JOURNAL,
            NO AFTER JOURNAL,
            CHECKSUM = DEFAULT,
            DEFAULT MERGEBLOCKRATIO,
            MAP = TD_MAP1
            (
                CREATION_DATE TIMESTAMP(6) WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
                ID VARCHAR(36) NOT NULL,
                ID_MODEL VARCHAR(36) NOT NULL,
                ID_MAPPER VARCHAR(36) NOT NULL,
                FEATURE_ENGINEERING_TYPE VARCHAR(255) NOT NULL,
                METADATA JSON(32000)
            )
            PRIMARY INDEX (ID);
            """
        return query

    def list_feature_engineering_models(self):
        """
        List the hyper models in the TDStone system.

        Returns:
            DataFrame: A DataFrame with the hyper model details.
        """

        query = 'SELECT * \n'

        query = query + f'\n FROM {self.schema_name}.{self.feature_engineering_process_repository}'

        return tdml.DataFrame.from_query(query)

    @execute_query
    def remove_feature_engineering_models(self, feature_engineering_process_id):
        """
        Remove a hyper model from the TDStone system.

        Args:
            model_id (str or list): The ID or list of IDs of the mapper to be removed.

        Returns:
            query: SQL query to remove the model.
        """
        if type(feature_engineering_process_id) == list and len(feature_engineering_process_id) > 0:
            feature_engineering_process_list = ",".join(["'" + x + "'" for x in feature_engineering_process_id])
            query = f"""
                DELETE {self.schema_name}.{self.feature_engineering_process_repository} WHERE ID IN ({feature_engineering_process_list});
                """
        else:
            query = f"""
                DELETE {self.schema_name}.{self.feature_engineering_process_repository} WHERE ID = '{feature_engineering_process_id}';
                """

        return query