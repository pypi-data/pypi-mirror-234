
from typing import Dict

from dftools.core.structure import BaseFieldDecoder, BaseStructureDecoder, Field, FieldCharacterisationStd, Namespace, Structure
from dftools.core.structure.decoder.field_decoder import BaseFieldDecoder

class SnowFieldDecoder(BaseFieldDecoder): 
    def __init__(self):
        super().__init__()

    def decode_json(self, input_data : Dict[str, str]) -> Field :
        data_type : str = input_data['DATA_TYPE']
        
        length = input_data['NUMERIC_PRECISION']
        if data_type == 'TEXT':
            length = input_data['CHARACTER_MAXIMUM_LENGTH']
        elif data_type.startswith('TIMESTAMP'):
            length = 29
        elif data_type == 'BINARY':
            length = 65536
        if length is None : length = 0

        precision = input_data['NUMERIC_PRECISION_RADIX']
        if data_type == 'TEXT':
            precision = 0
        elif data_type.startswith('TIMESTAMP'):
            precision = input_data['DATETIME_PRECISION']
        elif data_type == 'BINARY':
            precision = 0
        if precision is None : precision = 0

        characterisations = []
        if input_data['PK'] == 1:
            characterisations.append(FieldCharacterisationStd.TEC_ID)

        return Field(name = input_data['FIELD_NAME']
            , desc = input_data['FIELD_COMMENT']
            , position=input_data['ORDINAL_POSITION']
            , data_type=data_type
            , length=length
            , precision=precision
            , default_value=input_data['DEFAULT_VALUE']
            , characterisations=characterisations
        )

class SnowStructureDecoder(BaseStructureDecoder):
    def __init__(self):
        super().__init__(SnowFieldDecoder())
    
    def decode_json(self, input_data : Dict[str, str]) -> (Namespace, Structure) :
        structure = Structure(name = input_data['STRUCTURE_NAME']
            , desc = input_data['STRUCTURE_DESCRIPTION']
            , type = input_data['STRUCTURE_TYPE']
            , row_count = input_data['ROW_COUNT']
            , options = {}
            , content_type= None
            , fields = []
            , sourcing_info = None
            )
        column_list = input_data['COLUMNS']
        for column_data in column_list:
            ''' As the fields are potentially provided in the wrong order, a check on fields is prevented '''
            structure.add_field(
                new_field=self.field_decoder.decode_json(column_data)
                , prevent_position_check=True
                )
        structure.sort_fields_by_ordinal_position()
        return (None, structure)
    
