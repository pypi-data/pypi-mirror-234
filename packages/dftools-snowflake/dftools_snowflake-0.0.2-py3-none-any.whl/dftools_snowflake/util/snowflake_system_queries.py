

SNOW_STRUCTURE_SELECT_QUERY = """SELECT 
    OBJECT_CONSTRUCT_KEEP_NULL(
        'DATABANK_TYPE', 'SNOWFLAKE'
        , 'STRUCTURE_TYPE', TAB.TABLE_TYPE  
        , 'DATABASE_NAME', TAB.TABLE_CATALOG
        , 'TABLE_SCHEMA', TAB.TABLE_SCHEMA
        , 'STRUCTURE_NAME', TAB.TABLE_NAME
        , 'STRUCTURE_DESCRIPTION', MAX(TAB.COMMENT)
        , 'STRUCTURE_CREATED', MAX(TAB.CREATED)
        , 'STRUCTURE_LAST_ALTERED', MAX(TAB.LAST_ALTERED)
        , 'STRUCTURE_OWNER', MAX(TAB.TABLE_OWNER)
        , 'ROW_COUNT', MAX(TAB.ROW_COUNT)
        , 'COLUMNS', ARRAY_AGG(
            OBJECT_CONSTRUCT_KEEP_NULL(
                'FIELD_NAME', COL.COLUMN_NAME
                , 'FIELD_COMMENT', COL.COMMENT
                , 'DATA_TYPE', COL.DATA_TYPE
                , 'ORDINAL_POSITION', COL.ORDINAL_POSITION
                , 'NUMERIC_PRECISION', COL.NUMERIC_PRECISION
                , 'NUMERIC_PRECISION_RADIX', COL.NUMERIC_PRECISION_RADIX
                , 'NUMERIC_SCALE', COL.NUMERIC_SCALE
                , 'CHARACTER_MAXIMUM_LENGTH', COL.CHARACTER_MAXIMUM_LENGTH
                , 'DATETIME_PRECISION', COL.DATETIME_PRECISION
                , 'IS_NULLABLE', COL.IS_NULLABLE
                , 'DEFAULT_VALUE', COL.COLUMN_DEFAULT
                , 'IS_IDENTITY', COL.IS_IDENTITY
                , 'IS_SELF_REFERENCING', COL.IS_SELF_REFERENCING
                , 'PK', CASE WHEN PK_INFO."database_name" IS NOT NULL THEN 1 ELSE 0 END
            )
            )
        )
FROM INFORMATION_SCHEMA.TABLES TAB
    INNER JOIN INFORMATION_SCHEMA.COLUMNS COL ON (
        TAB.TABLE_CATALOG = COL.TABLE_CATALOG
    AND TAB.TABLE_SCHEMA = COL.TABLE_SCHEMA
    AND TAB.TABLE_NAME = COL.TABLE_NAME
    )
    LEFT OUTER JOIN DATA_STRUCTURE_PRIMARY_KEYS PK_INFO ON (
        PK_INFO."database_name" = COL.TABLE_CATALOG
    AND PK_INFO."schema_name" = COL.TABLE_SCHEMA
    AND PK_INFO."table_name" = COL.TABLE_NAME
    AND PK_INFO."column_name" = COL.COLUMN_NAME
    )
{0}
GROUP BY 
        TAB.TABLE_TYPE  
        , TAB.TABLE_CATALOG
        , TAB.TABLE_SCHEMA
        , TAB.TABLE_NAME
;
"""

def get_snow_structure_query_for_catalog_namespace_and_table(catalog : str, namespace : str, table_name : str) -> str:
    return SNOW_STRUCTURE_SELECT_QUERY.format("WHERE TAB.TABLE_CATALOG = '" + catalog + "' AND TAB.TABLE_SCHEMA = '" + namespace + "' AND TAB.TABLE_NAME = '" + table_name + "'")

def get_snow_structure_query_for_namespace_and_table(namespace : str, table_name : str) -> str:
    return SNOW_STRUCTURE_SELECT_QUERY.format("WHERE TAB.TABLE_SCHEMA = '" + namespace + "' AND TAB.TABLE_NAME = '" + table_name + "'")

def get_snow_structure_query_for_catalog_and_namespace(catalog : str, namespace : str) -> str:
    return SNOW_STRUCTURE_SELECT_QUERY.format("WHERE TAB.TABLE_CATALOG = '" + catalog + "' AND TAB.TABLE_SCHEMA = '" + namespace + "'")

def get_snow_structure_query_for_namespace(namespace : str) -> str:
    return SNOW_STRUCTURE_SELECT_QUERY.format("WHERE TAB.TABLE_SCHEMA = '" + namespace + "'")