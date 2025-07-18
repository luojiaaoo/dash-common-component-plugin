from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text(encoding='utf-8')
setup(
    name='dash-common-component-plugin',
    version='0.1.0',
    install_requires=[
        'dash>=3.1.1',
        'feffery-antd-components>=0.4',
        'feffery-utils-components>=0.3',
        'yarl',
    ],
    packages=['dash_common_component_plugin'],
    author='NOKIAO',
    description='A plugin to inject common component, like message/relocate etc...',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/luojiaaoo/dash-common-component-plugin',
)
