
import snowflake
from datetime import datetime

from dftools.events import StandardErrorEvent, StandardExtendedInfoEvent
from dftools.core.database import ConnectionWrapper, QueryExecResult
from dftools.core.structure import Namespace
from dftools_snowflake.util import SnowflakeUtil as SnowUtil

from dftools_snowflake.connection.snowflake_connection_info import SnowflakeConnectionInfo, SnowflakeConnectionSchemaInfo

class SnowflakeConnectionWrapper(ConnectionWrapper):

    def __init__(self, connection_info : SnowflakeConnectionInfo, schema_info : SnowflakeConnectionSchemaInfo = None) -> None:
        """
        Creates a new connection wrapper for Snowflake, storing the current connection information state and initialises the connection

        Parameters
        -----------
            connectionInfo: The snowflake connection information. This parameter is mandatory
            schemaInfo : The snowflake schema information
        """
        super().__init__()
        self.connection_info = connection_info
        self.conn = connection_info.create_new_connection()
        self.set_snowflake_connection_schema_info(schema_info)

    def set_snowflake_connection_schema_info(self, schema_info : SnowflakeConnectionSchemaInfo) -> None:
        """
        Sets the Snowflake Connection Schema Information object and updates the connection current connection schema information.

        Parameters
        -----------
            schemaInfo : The snowflake schema information to apply on connection
        """
        self.schema_info = schema_info
        if self.schema_info is not None :
            self.update_connection_schema_info()

    # Connection methods
    def get_current_catalog(self) -> str:
        return self.get_schema_info().db
    
    def get_current_namespace_name(self) -> str:
        return self.get_schema_info().schema

    def get_current_namespace(self) -> Namespace:
        return Namespace(databank_name='Snowflake', catalog=self.get_current_catalog(), namespace=self.get_current_namespace_name())
    
    def close_connection(self):
        return self.conn.close()
    
    # Snowflake specific methods

    def get_cursor(self):
        """
        Sets the Snowflake Connection Schema Information object and updates the connection current connection schema information.

        Returns
        -----------
            cursor : A cursor on the current connection stored in this wrapper
        """
        return self.conn.cursor()

    def get_schema_info(self) -> SnowflakeConnectionSchemaInfo:
        """
        Get the Snowflake Connection Schema Information object

        Returns
        -----------
            snowflake_connection_schema_info : The Snowflake Connection Schema Information
        """
        return self.schema_info
    
    def has_schema_info(self) -> SnowflakeConnectionSchemaInfo:
        """
        Checks if the Snowflake Connection Schema Information object is available

        Returns
        -----------
            True if schema information is available, False otherwise
        """
        return self.schema_info is not None

    def get_schema(self):
        """
        Get the Schema object

        Returns
        -----------
            schema_info : The Schema
        """
        return self.get_schema_info().schema if self.has_schema_info() else None
    
    def has_schema(self):
        """
        Checks if schema is available on this connection

        Returns
        -----------
            True if schema is available, False otherwise
        """
        return self.get_schema() is not None
    
    def log_execution_error(self, error : snowflake.connector.errors.ProgrammingError) -> None:
        self.log_event(StandardErrorEvent(SnowUtil.get_standard_error_message(error)))

    def update_connection_schema_info(self):
        """
        Update the connection schema information stored in this wrapper and updates the connection.
        """
        cur = self.get_cursor()
        if self.schema_info.role is None :
            cur.close()
            return
        
        query = f"USE ROLE {self.schema_info.role}"
        query_result = self.execute_query(query)
        if query_result.is_error() : 
            raise RuntimeError("Role " + self.schema_info.role + " cannot be set")
        
        if self.schema_info.warehouse is not None :
            query = f"USE WAREHOUSE {self.schema_info.warehouse}"
            query_result = self.execute_query(query)
            if query_result.is_error() : 
                raise RuntimeError("Warehouse " + self.schema_info.warehouse + " cannot be set")
        
        if self.schema_info.db is not None :
            query = f"USE DATABASE {self.schema_info.db}"
            query_result = self.execute_query(query)
            if query_result.is_error() : 
                raise RuntimeError("Database " + self.schema_info.db + " cannot be set")
            
            if self.schema_info.schema is not None:
                query = f"USE SCHEMA {self.schema_info.schema}"
                query_result = self.execute_query(query)
                if query_result.is_error() : 
                    raise RuntimeError("Schema " + self.schema_info.schema + " cannot be set")
        
        cur.close()
    
    # Query and script execution methods
    def execute_query(self, query : str, name : str = '') -> QueryExecResult:
        cur = self.get_cursor()
        start_tst = datetime.now()
        try:
            cur.execute(query)
            query_id = cur.sfqid
            return QueryExecResult(name, QueryExecResult.SUCCESS, query, query_id, list(cur)
                , SnowUtil.get_structure_from_result_metadata(cur.description), start_tst, datetime.now())
        except snowflake.connector.errors.ProgrammingError as e:
            self.log_execution_error(e)
            return QueryExecResult(name, QueryExecResult.ERROR, query, e.sfqid, [SnowUtil.get_standard_error_message(e)]
                , SnowUtil.get_structure_for_error_result(), start_tst, datetime.now())
        finally:
            cur.close()
                
    def write_query_result_to_file(self, query: str, target_file_path : str) -> None:
        """
        Executes a query on the snowflake connection contained in the wrapper and creates a file with the result

        Parameters
        -----------
            query : str
                The query to execute
            target_file_path : str
                The target file name path
        """
        query_result = self.execute_query(query)
        if query_result.is_success() :
            SnowUtil.write_result_set_to_file(
                file_path=target_file_path
                , result_set=query_result.result_set
                , result_set_structure=query_result.result_set_structure
            )
        else :
            self.log_event(StandardExtendedInfoEvent('No file generated as the query execution failed. Check query execution error message for more information.'))
        return query_result

