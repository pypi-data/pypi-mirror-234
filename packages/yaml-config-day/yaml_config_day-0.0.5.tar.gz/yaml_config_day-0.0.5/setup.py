from setuptools import setup, find_packages

setup(
    name='yaml_config_day',
    version='0.0.5',
    description='A Python library for managing project yaml secrets configurations',
    author='John Major',
    author_email='john@daylilyinformatics.com',
    url='https://github.com/Daylily-Informatics/yaml_config_day',
    packages=find_packages(),
    install_requires=[
        'pyyaml', 
    ],
    entry_points={
        'console_scripts': [
            'yaml_config_day = yaml_config_day.config_manager:main', 
        ],
    },
)
