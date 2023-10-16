from os import path
import os
import pathlib
import re
import shutil
from typing import List, Type
import unittest

from src.confluent import Orchestrator
from src.confluent.base.language_config_base import LanguageConfigBase
from src.confluent.base.language_type import LanguageType
from src.confluent.generators.java_generator import JavaGenerator
from src.confluent.generators.javascript_generator import JavascriptGenerator
from src.confluent.generators.typescript_generator import TypescriptGenerator
from src.confluent.generators.python_generator import PythonGenerator
from src.confluent.generators.c_generator import CGenerator
from src.confluent.generators.go_generator import GoGenerator
from src.confluent.language_configs.java_config import JavaConfig
from src.confluent.language_configs.javascript_config import JavascriptConfig
from src.confluent.language_configs.typescript_config import TypescriptConfig
from src.confluent.language_configs.python_config import PythonConfig
from src.confluent.language_configs.c_config import CConfig
from src.confluent.language_configs.go_config import GoConfig


_CONFLUENT_REFERENCE_REGEX = r'Generated with confluent v\d+\.\d+\.\d+'


class TestGenerator(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._test_path = pathlib.Path(__file__).parent.resolve()
        self._test_config_path = path.join(self._test_path, '..', 'example/test-config.yaml')
        self._test_compare_files_path = path.join(self._test_path, 'compare_files')

    def test_read_config(self):
        orchestrator = Orchestrator.read_config(self._test_config_path)
        self._evaluate_configs(orchestrator.language_configs)

    def test_parse_config(self):
        TEST_INCLUDE = 'test-include.yaml'

        with open(self._test_config_path, 'r') as f:
            content = f.read().replace(TEST_INCLUDE, os.path.join(os.getcwd(), 'example', TEST_INCLUDE))
        orchestrator = Orchestrator.parse_config(content, 'test-config')
        self._evaluate_configs(orchestrator.language_configs)

    def test_run_generators(self):
        orchestrator = Orchestrator.read_config(self._test_config_path)

        for config in orchestrator.language_configs:
            compare_file_path = path.join(
                self._test_compare_files_path,
                f'{config.config_info.file_name_full}'
            )
            
            with open(compare_file_path, 'r') as f:
                content = f.read()

            original_max_diff = self.maxDiff
            self.maxDiff = None
            self.assertEqual(
                # Remove versions to keep tests working if version changed.
                re.sub(_CONFLUENT_REFERENCE_REGEX, '', config.dump()), 
                re.sub(_CONFLUENT_REFERENCE_REGEX, '', content),
            )
            self.maxDiff = original_max_diff

    def test_write_configs(self):
        OUTPUT_DIR = path.join(self._test_path, 'test_output')
        orchestrator = Orchestrator.read_config(self._test_config_path)

        if not os.path.isdir(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        
        # Write all configs to the output folder.
        orchestrator.write(OUTPUT_DIR)

        # Collect the output file names.
        files = os.listdir(OUTPUT_DIR)

        # Cleanup output directory.
        shutil.rmtree(OUTPUT_DIR)

        # Compare files.
        for config in orchestrator.language_configs:
            self.assertIn(config.config_info.file_name_full, files)

    def _evaluate_configs(self, configs: List[LanguageConfigBase]):
        checks = [
            # Check Java config.
            [self._evaluate_java_properties, 'TestConfig'],

            # Check JavaScript config.
            [self._evaluate_javascript_properties, 'TEST_CONFIG'],

            # Check TypeScript config.
            [self._evaluate_typescript_properties, 'test-config'],

            # Check Python config.
            [self._evaluate_python_properties, 'test_config'],

            # Check C config.
            [self._evaluate_c_properties, 'test_config'],

            # Check Go config.
            [self._evaluate_go_properties, 'test_config'],
        ]

        self.assertIsNotNone(configs)
        self.assertIsInstance(configs, list)
        self.assertEqual(len(configs), len(checks))

        # Check the languages.
        for i, check in enumerate(checks):
            check[0](configs[i], check[1])

    def _evaluate_java_properties(self, config: JavaConfig, name: str):
        self._evaluate_common_properties(config, 'java', name, LanguageType.JAVA, JavaGenerator)
        self.assertEqual(config.generator.package, 'my.test.package')

    def _evaluate_javascript_properties(self, config: JavascriptConfig, name: str):
        self._evaluate_common_properties(config, 'js', name, LanguageType.JAVASCRIPT, JavascriptGenerator)

    def _evaluate_typescript_properties(self, config: TypescriptConfig, name: str):
        self._evaluate_common_properties(config, 'ts', name, LanguageType.TYPESCRIPT, TypescriptGenerator)

    def _evaluate_python_properties(self, config: PythonConfig, name: str):
        self._evaluate_common_properties(config, 'py', name, LanguageType.PYTHON, PythonGenerator)

    def _evaluate_c_properties(self, config: CConfig, name: str):
        self._evaluate_common_properties(config, 'h', name, LanguageType.C, CGenerator)

    def _evaluate_go_properties(self, config: GoConfig, name: str):
        self._evaluate_common_properties(config, 'go', name, LanguageType.GO, GoGenerator)
        self.assertEqual(config.generator.package, 'myconfig')

    def _evaluate_common_properties(
        self,
        config: LanguageConfigBase,
        extension: str,
        name: str,
        type: LanguageType,
        generator_type: Type
    ):
        self.assertEqual(config.config_info.file_extension, extension)
        self.assertEqual(config.config_info.file_name, name)
        self.assertEqual(config.language_type, type)
        self.assertEqual(config.generator.__class__, generator_type)
