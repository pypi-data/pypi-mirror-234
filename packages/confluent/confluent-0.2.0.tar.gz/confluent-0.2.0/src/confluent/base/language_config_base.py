from __future__ import annotations
from abc import ABC, abstractmethod
import re
from typing import List, Type

from .configuration_base import _DEFAULT_INDENT
from .generator_base import GeneratorBase
from .language_type import LanguageType
from .language_config_configuration import LanguageConfigConfiguration
from .language_config_naming_conventions import LanguageConfigNamingConventions
from .config_file_info import ConfigFileInfo
from .name_converter import NameConverter
from .property import Property


class InvalidFileNameException(Exception):
    def __init__(self, file_name: str, pattern: str):
        super().__init__(f'The file name "{file_name}" does not conform to the validation pattern "{pattern}"')


class LanguageConfigBase(ABC):
    """
    Abstract class which serves as the base for all language specific config classes. The LanguageConfigBase holds all
    required information (language type, naming convention, generator, ...) to generate a config file.
    """

    def __init__(
        self,
        config_name: str,
        properties: List[Property],
        indent: int = _DEFAULT_INDENT,
        transform: str = None,
        naming_conventions: LanguageConfigNamingConventions = None,
        additional_props = {},
    ):
        """
        Constructor

        :param config:           Language config configuration.
        :type config:            LanguageConfigConfiguration
        :param properties:       Which properties to generate.
        :type properties:        List[Property]
        :param additional_props: Additional props which might be required by the deriving generator class,
                                 defaults to {}
        :type additional_props:  dict, optional
        """
        config = LanguageConfigConfiguration(
            config_name=config_name,
            language_type=self._language_type(),
            file_extension=self._file_extension(),
            generator_type=self._generator_type(),
            indent=indent,
            transform=transform,
            naming_conventions=naming_conventions,
        )

        # Make sure, config is valid.
        config.validate()

        self.generator = config.generator_type(
            config.get_generator_config(),
            properties,
            additional_props,
        )
        self.config_info = ConfigFileInfo(
            # Convert config file name according to naming convention if a convention was provided. Otherwise, just use
            # the config name directly.
            NameConverter.convert(config.config_name, config.naming_conventions.file_naming_convention) if
                config.naming_conventions.file_naming_convention else
                config.config_name,

            config.file_extension,
        )
        self.language_type = config.language_type

        # Check output file naming.
        self._check_file_name()

    def dump(self) -> str:
        """
        Generates a config file string.

        :return: Config file string.
        :rtype:  str
        """
        return self.generator.dump()
    
    def write(self, path: str = '') -> LanguageConfigBase:
        """
        Generates a config file string and writes the config file to the provided directory.

        :param path: Directory to write the file to, defaults to ''
        :type path:  str, optional

        :return:     The current LanguageConfigBase instance.
        :rtype:      LanguageConfigBase
        """
        path = path.rstrip('/').rstrip('\\')  # Strip right-side slashes.
        path = f'{path}/{self.config_info.file_name_full}'

        with open(path, 'w') as f:
            f.write(self.dump())
        return self
    
    @abstractmethod
    def _language_type(self) -> LanguageType:
        pass

    @abstractmethod
    def _file_extension(self) -> str:
        pass

    @abstractmethod
    def _generator_type(self) -> Type[GeneratorBase]:
        pass
    
    @abstractmethod
    def _allowed_file_name_pattern(self) -> str:
        """
        Abstract method which must be implemented by the deriving class to provide a RegEx string which describes which
        file name patterns are allowed for the output file name (without extension).

        :return: Allowed file name pattern.
        :rtype:  str
        """
        pass

    def _check_file_name(self) -> None:
        """
        Checks if the config file name matches the pattern defined by the deriving class.

        :raises InvalidFileNameException: Thrown if the file name is not valid.
        """
        pattern = self._allowed_file_name_pattern()

        if not re.match(pattern, self.config_info.file_name):
            raise InvalidFileNameException(self.config_info.file_name, pattern)
