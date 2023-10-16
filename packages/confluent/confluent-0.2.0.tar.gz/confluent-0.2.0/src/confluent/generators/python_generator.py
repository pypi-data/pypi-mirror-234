from ..base.name_converter import NamingConventionType
from ..base.generator_base import GeneratorBase
from ..base.property import Property
from ..base.property_type import PropertyType


class PythonGenerator(GeneratorBase):
    """
    Python specific generator. For more information about the generator methods, refer to GeneratorBase.
    """

    def _default_type_naming_convention(self) -> NamingConventionType:
        return NamingConventionType.PASCAL_CASE
    
    def _before_type(self) -> str:
        return ''

    def _property_before_type(self, _: Property) -> str:
        return ''
    
    def _start_type(self, type_name: str) -> str:
        return f'class {type_name}:'

    def _property_in_type(self, property: Property) -> str:
        match property.type:
            case PropertyType.BOOL:
                value = 'True' if property.value else 'False'
            case PropertyType.INT | PropertyType.FLOAT | PropertyType.DOUBLE:
                value = property.value
            case PropertyType.STRING:
                value = property.value.replace('\\', '\\\\')  # TODO: Might need to be refined.
                value = f'\'{value}\''  # Wrap in single quotes.
            case PropertyType.REGEX:
                value = f'r\'{property.value}\''  # Wrap in single quotes.
            case _:
                raise Exception('Unknown type')

        return f'{property.name} = {value}'
    
    def _property_comment(self, comment: str) -> str:
        return f'  # {comment}'
    
    def _end_type(self) -> str:
        return ''
    
    def _property_after_type(self, _: Property) -> str:
        return ''
    
    def _after_type(self) -> str:
        return ''
