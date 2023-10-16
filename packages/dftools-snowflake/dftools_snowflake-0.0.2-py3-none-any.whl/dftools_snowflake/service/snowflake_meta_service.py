
from dftools.core.database import DatabaseMetadataService
from dftools_snowflake.util.snowflake_system_queries import (
    get_snow_structure_query_for_namespace
    , get_snow_structure_query_for_catalog_and_namespace
    , get_snow_structure_query_for_namespace_and_table
    , get_snow_structure_query_for_catalog_namespace_and_table
)
from dftools_snowflake.connection import SnowflakeConnectionWrapper
from dftools_snowflake.service.meta_decoder import SnowStructureDecoder

class SnowMetadataService(DatabaseMetadataService):
    def __init__(self, connection_wrapper: SnowflakeConnectionWrapper) -> None:
        super().__init__(connection_wrapper, SnowStructureDecoder())
    
    def get_structure_from_database(self, namespace : str, table_name : str, catalog : str = None) -> list:
        data_structure_extract_query = get_snow_structure_query_for_namespace_and_table(namespace=namespace, table_name=table_name) \
            if catalog is None else get_snow_structure_query_for_catalog_namespace_and_table(catalog=catalog, namespace=namespace, table_name=table_name)
        query_result = self.conn_wrap.execute_query("SHOW PRIMARY KEYS;")
        self.conn_wrap.execute_query(
            f"CREATE OR REPLACE TEMPORARY TABLE DATA_STRUCTURE_PRIMARY_KEYS AS SELECT * FROM TABLE(RESULT_SCAN('{query_result.query_id}'));")
        query_result = self.conn_wrap.execute_query(data_structure_extract_query)
        return query_result.result_set[0]

    def get_structures_from_database(self, namespace : str, catalog : str = None) -> list:
        data_structure_extract_query = get_snow_structure_query_for_namespace(namespace=namespace) if catalog is None \
            else get_snow_structure_query_for_catalog_and_namespace(catalog=catalog, namespace=namespace)
        query_result = self.conn_wrap.execute_query("SHOW PRIMARY KEYS;")
        self.conn_wrap.execute_query(
            f"CREATE OR REPLACE TEMPORARY TABLE DATA_STRUCTURE_PRIMARY_KEYS AS SELECT * FROM TABLE(RESULT_SCAN('{query_result.query_id}'));")
        query_result = self.conn_wrap.execute_query(data_structure_extract_query)
        return query_result.result_set