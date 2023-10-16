from __future__ import annotations
import os
from typing import List, Tuple, Type

import yaml
from schema import Schema, Use, Optional, Or

from .config_language_mapping import ConfigLanguageMapping
from .name_converter import NamingConventionType
from .property import Property
from .property_type import PropertyType
from .language_type import LanguageType
from .language_config_base import LanguageConfigBase
from .language_config_naming_conventions import LanguageConfigNamingConventions

# Main categories.
_KEY_INCLUDES = 'includes'
_KEY_LANGUAGES = 'languages'
_KEY_PROPERTIES = 'properties'

# Include keys.
_KEY_PATH = 'path'
_KEY_AS = 'as'

# Language keys.
_KEY_FILE_NAMING = 'file_naming'
_KEY_PROPERTY_NAMING = 'property_naming'
_KEY_TYPE_NAMING = 'type_naming'
_KEY_INDENT = 'indent'
_KEY_TRANSFORM = 'transform'
_KEY_TYPE = 'type'
_KEY_NAME = 'name'

# Property keys.
_KEY_VALUE = 'value'
_KEY_HIDDEN = 'hidden'
_KEY_COMMENT = 'comment'

# Load the glue.
_LANGUAGE_MAPPINGS = ConfigLanguageMapping.get_mappings()


class UnknownPropertyTypeException(Exception):
    def __init__(self, property_type: str):
        super().__init__(f'Unknown property type {property_type}')


class UnknownLanguageException(Exception):
    def __init__(self, language: str):
        super().__init__(f'Unknown language {language}')


class SeveralLanguagesException(Exception):
    def __init__(self, language: str):
        super().__init__(f'Several languages matched for {language}')


class NoLanguageConfigException(Exception):
    def __init__(self, language_type: LanguageType):
        super().__init__(f'No language config found for {language_type}')


class SeveralLanguageConfigsException(Exception):
    def __init__(self, language_type: LanguageType):
        super().__init__(f'Several languages configs found for {language_type}')


class AliasAlreadyInUseException(Exception):
    def __init__(self, alias: str):
        super().__init__(f'The include-alias \'{alias}\' is already in use')


class Config:
    """
    Handles the config evaluation by parsing the provided YAML string via the parse-method.
    """

    @staticmethod
    def read(path: str) -> List[LanguageConfigBase]:
        """
        Reads the provided YAML configuration file and generates a list of language configurations.

        :param path: Path to load the YAML file from (see example/test-config.yaml for configuration details).
        :type path:  str

        :return: Language configurations which further can be dumped as config files.
        :rtype:  List[LanguageConfigBase]
        """
        return Config._read(path)[0]

    @staticmethod
    def parse(content: str, config_name: str) -> List[LanguageConfigBase]:
        """
        Parses the provided YAML configuration string and returns the corresponding language configurations.

        :param content:     YAML configuration strings. For config details, please check the test-config.yaml in
                            the example folder.
        :type content:      str
        :param config_name: Output config file name. NOTE: The actual file name format might be overruled by
                            the specified file_naming rule from the config.
        :type config_name:  str

        :return: Language configurations which further can be dumped as config files.
        :rtype:  List[LanguageConfigBase]
        """
        return Config._parse(content, config_name)[0]

    @staticmethod
    def _read(path: str, namespace: str='', namespaces: List[str]=None) -> List[LanguageConfigBase]:
        """
        Reads the provided YAML configuration file and generates a list of language configurations.

        :param path:      Path to load the YAML file from (see example/test-config.yaml for configuration details).
        :type path:       str
        :param namespace: Specifies a namespace for the config. If None or empty, no namespace will be set.
        :type nammespace: str

        :return: Language configurations which further can be dumped as config files.
        :rtype:  List[LanguageConfigBase]
        """
        with open(path, 'r') as f:
            content = f.read()

        # Prepare config name.
        last_part = path.replace(r'\\', '/').split('/')[-1]

        if '.' in last_part:
            config_name = '.'.join(last_part.split('.')[0:-1])
        else:
            config_name = last_part
        return Config._parse(content, config_name, namespace, os.path.dirname(path), namespaces)

    @staticmethod
    def _parse(content: str, config_name: str, namespace: str='', directory: str='', namespaces: List[str]=None) -> \
        Tuple[List[LanguageConfigBase], List[Property]]:
        """
        Parses the provided YAML configuration string and returns the corresponding language configurations.

        :param content:     YAML configuration strings. For config details, please check the test-config.yaml in
                            the example folder.
        :type content:      str
        :param config_name: Output config file name. NOTE: The actual file name format might be overruled by
                            the specified file_naming rule from the config.
        :type config_name:  str
        :param namespace:   Specifies a namespace for the config. If None or empty, no namespace will be set.
        :type nammespace:   str

        :raises AliasAlreadyInUseException: Raised if an included config file uses an already defined alias.

        :return: Language configurations which further can be dumped as config files.
        :rtype:  List[LanguageConfigBase]
        """
        yaml_object = yaml.safe_load(content)
        validated_object = Config._schema().validate(yaml_object)
        language_configs: List[LanguageConfigBase] = []
        properties: List[Property] = []

        # Since a default list cannot be assigned to the namespaces variable in the method header, because it only
        # gets initialized once and then the list gets re-used (see https://stackoverflow.com/a/1145781), make sure
        # that namespaces gets set to a freshly created list if it hasn't already been until now.
        if not namespaces:
            namespaces = []

        # Collect properties as they are the same for all languages.
        for property in validated_object[_KEY_PROPERTIES]:
            properties.append(Property(
                name=property[_KEY_NAME],
                value=property[_KEY_VALUE],
                property_type=property[_KEY_TYPE],
                hidden=property[_KEY_HIDDEN] if _KEY_HIDDEN in property else None,
                comment=property[_KEY_COMMENT] if _KEY_COMMENT in property else None,
                namespace=namespace,
            ))

        # Evaluate included files and their properties.
        if _KEY_INCLUDES in validated_object:
            for inclusion in validated_object[_KEY_INCLUDES]:
                inclusion_namespace = inclusion[_KEY_AS]

                # Make sure that a included config file does not re-define an alias.
                if inclusion_namespace in namespaces:
                    raise AliasAlreadyInUseException(inclusion_namespace)
                else:
                    namespaces.append(inclusion_namespace)
                inclusion_path = inclusion[_KEY_PATH]

                # If the provided path is relative, incorporate the provided directory into the path.
                if not os.path.isabs(inclusion_path):
                    inclusion_path = os.path.join(directory, inclusion_path)

                # Read included config and put properties into property list.
                for inclusion_property in Config._read(inclusion_path, inclusion_namespace, namespaces)[1]:
                    inclusion_property.hidden = True  # Included properties are not being exported by default.
                    properties.append(inclusion_property)

        # Evaluate each language setting one by one.
        if _KEY_LANGUAGES in validated_object:
            for language in validated_object[_KEY_LANGUAGES]:
                naming_conventions = LanguageConfigNamingConventions()
                language_type = language[_KEY_TYPE]
                indent = language[_KEY_INDENT] if _KEY_INDENT in language else None
                transform = language[_KEY_TRANSFORM] if _KEY_TRANSFORM in language else None

                # Evaluate file naming-convention.
                naming_conventions.file_naming_convention = Config._evaluate_naming_convention_type(
                    language[_KEY_FILE_NAMING] if _KEY_FILE_NAMING in language else None
                )

                # Evaluate properties naming-convention.
                naming_conventions.properties_naming_convention = Config._evaluate_naming_convention_type(
                    language[_KEY_PROPERTY_NAMING] if _KEY_PROPERTY_NAMING in language else None
                )

                # Evaluate type naming-convention.
                naming_conventions.type_naming_convention = Config._evaluate_naming_convention_type(
                    language[_KEY_TYPE_NAMING] if _KEY_TYPE_NAMING in language else None
                )
                config_type = Config._evaluate_config_type(language_type)

                language_configs.append(config_type(
                    config_name=config_name,
                    properties=properties,
                    indent=indent,
                    transform=transform,
                    naming_conventions=naming_conventions,

                    # Pass all language props as additional_props to let the specific
                    # generator decide which props it requires additionally.
                    additional_props=language,
                ))

        return language_configs, properties
    
    @staticmethod
    def _schema() -> Schema:
        """
        Returns the config validation schema.

        :return: Config validation schema.
        :rtype:  Schema
        """
        return Schema({
            Optional(_KEY_INCLUDES): [{
                _KEY_PATH: str,
                _KEY_AS: str,
            }],
            Optional(_KEY_LANGUAGES): [{
                _KEY_TYPE: Use(Config._evaluate_language_type),
                Optional(_KEY_FILE_NAMING): str,
                Optional(_KEY_INDENT): int,
                Optional(object): object  # Collect other properties(?).
            }],
            _KEY_PROPERTIES: [{
                _KEY_TYPE: Use(Config._evaluate_data_type),
                _KEY_NAME: str,
                _KEY_VALUE: Or(str, bool, int, float),
                Optional(_KEY_HIDDEN): bool,
                Optional(_KEY_COMMENT): str,
            }]
        })
    
    @staticmethod
    def _evaluate_data_type(type: str) -> PropertyType:
        """
        Evaluates a properties data type.

        :param type: Property type string (e.g., bool | string | ...).
        :type type:  str

        :raises UnknownPropertyTypeException: Raised if an unsupported property type was used in the config.

        :return: The corresponding PropertyType enum value.
        :rtype:  PropertyType
        """
        try:
            type = PropertyType(type)
        except ValueError:
            raise UnknownPropertyTypeException(type)
        return type

    @staticmethod
    def _evaluate_language_type(language: str) -> LanguageType:
        """
        Evaluates the requested language type.

        :param language: Language to generate a config for (e.g., java | typescript | ...).
        :type language:  str

        :raises UnknownLanguageException:  Raised if an unsupported language was used in the config.
        :raises SeveralLanguagesException: Raised if several mappings were found for the requested language. If this
                                           error arises, it's a package error. Please open an issue at
                                           https://github.com/monstermichl/confluent/issues.

        :return: The corresponding LanguageType enum value.
        :rtype:  LanguageType
        """
        found = [mapping.type for mapping in _LANGUAGE_MAPPINGS if mapping.name == language]
        length = len(found)

        if length == 0:
            raise UnknownLanguageException(language)
        elif length > 1:
            raise SeveralLanguagesException(language)
        return found[0]
    
    @staticmethod
    def _evaluate_config_type(language_type: LanguageType) -> Type[LanguageConfigBase]:
        """
        Evaluates the languages config type to use for further evaluation.

        :param language_type: Language type to search the corresponding language config for (e.g., LanguageType.JAVA).
        :type language_type:  LanguageType

        :raises NoLanguageConfigException:       Raised if no language config mapping was provided for the specified
                                                 language type. If this error arises, it's a package error. Please open
                                                 an issue at https://github.com/monstermichl/confluent/issues.
        :raises SeveralLanguageConfigsException: Raised if several language config mappings were found for the specified
                                                 language type. If this error arises, it's a package error. Please open
                                                 an issue at https://github.com/monstermichl/confluent/issues.

        :return: The corresponding LanguageConfigBase derivate type (e.g., Type[JavaConfig]).
        :rtype:  Type[LanguageConfigBase]
        """
        found = [mapping.config_type for mapping in _LANGUAGE_MAPPINGS if mapping.type == language_type]
        length = len(found)

        if length == 0:
            raise NoLanguageConfigException(language_type)
        elif length > 1:
            raise SeveralLanguageConfigsException('Several language configs found')
        return found[0]
    
    @staticmethod
    def _evaluate_naming_convention_type(naming_convention: str) -> NamingConventionType:
        """
        Evaluates which naming convention type to use for the output file.

        :param naming_convention: Naming convention string (e.g., snake | camel | ...).
        :type naming_convention:  str

        :return: The corresponding NamingConventionType enum value.
        :rtype:  NamingConventionType
        """
        if naming_convention == 'snake':
            naming_convention = NamingConventionType.SNAKE_CASE
        elif naming_convention == 'screaming_snake':
            naming_convention = NamingConventionType.SCREAMING_SNAKE_CASE
        elif naming_convention == 'camel':
            naming_convention = NamingConventionType.CAMEL_CASE
        elif naming_convention == 'pascal':
            naming_convention = NamingConventionType.PASCAL_CASE
        elif naming_convention == 'kebap':
            naming_convention = NamingConventionType.KEBAP_CASE
        return naming_convention
