from pathlib import Path
from setuptools import setup, find_packages

# Setup process taken from here: https://www.freecodecamp.org/news/build-your-first-python-package/.

DESCRIPTION = 'confluent keeps your language specific configs in sync'
LONG_DESCRIPTION = Path(__file__).parent.absolute().joinpath('README.md').read_text()

# Get version.
try:
    with open('src/confluent/base/info.py') as fp:
        info = {}
        exec(fp.read(), info)
        VERSION = info['VERSION']
except Exception as e:
    print(e)
    exit(-1)

setup(
        name='confluent', 
        version=VERSION,
        author='monstermichl',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        package_dir={'': 'src'},
        packages=find_packages(where='src'),
        entry_points = {
            'console_scripts': ['confluent=src.config_generator:__main__'],
        },
        install_requires=[
            'pyyaml >= 6.0.1',
            'schema >= 0.7.5',
        ],
        extras_require={
            'dev': [
                'wheel>=0.41.1',
                'twine>=4.0.2',
                'ruff>=0.0.47',
                'coverage>=7.2.7',
            ],
        },
        python_requires='>=3.10',
        classifiers= [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        url = 'https://github.com/monstermichl/confluent.git',
        keywords = [
            'multi',
            'distributed',
            'configuration',
            'generator',
            'confluent',
            'languages',
            'distribution',
            'java',
            'javascript',
            'typescript',
            'python',
            'c',
            'go',
        ],
)
