
import snowflake.connector

class SnowflakeConnectionInfo():
    """
        Snowflake Connection Info
        
        A connection schema information is based on an account, a user and an authenticator method
        All these information are mandatory
    """
    def __init__(self, account : str, authenticator : str, user : str, password : str = None) -> None:
        self.account = account
        self.user = user
        self.authenticator = authenticator
        self.password = password

    def create_new_connection(self):
        """
        Creates a new Snowflake connection based on the connection info of this object

        Returns
        -----------
            The new Snowflake connection
        """
        return snowflake.connector.connect(
            account=self.account, user=self.user, authenticator=self.authenticator, password=self.password)

def create_snowflake_connection_info_from_dict(dict : dict) -> SnowflakeConnectionInfo:
    """
    Creates a new Snowflake connection info based on a dictionnary which contains key, value pair for keys :
    account, user, authenticator

    Parameters
    -----------
        dict : a dictionnary

    Returns
    -----------
        The new Snowflake connection Info
    """
    return SnowflakeConnectionInfo(
        account=dict['account']
        , authenticator=dict['authenticator']
        , user=dict['user']
        , password=dict['password'] if 'password' in dict.keys() else None)


class SnowflakeConnectionSchemaInfo():
    """
        Snowflake Connection Schema Information

        A connection schema information is based on a role, warehouse, database and schema.
        All these information are mandatory
    """
    def __init__(self, role: str, warehouse: str, db : str, schema : str) -> None:
        self.role=role
        self.warehouse=warehouse
        self.db=db
        self.schema=schema

def create_snowflake_connection_schema_info_from_dict(dict : dict) -> SnowflakeConnectionSchemaInfo:
    """
    Creates a new Snowflake connection info based on a dictionnary which contains key, value pair for keys :
    role, warehouse, db, schema

    Parameters
    -----------
        dict : a dictionnary

    Returns
    -----------
        The new Snowflake connection schema Info
    """
    return SnowflakeConnectionSchemaInfo(dict['role'], dict['warehouse'], dict['db'], dict['schema'])

