# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiges',
 'aiges.aiges_inner',
 'aiges.backup',
 'aiges.client',
 'aiges.client.utils',
 'aiges.cmd',
 'aiges.concurrent',
 'aiges.core',
 'aiges.examples.once.mmocr',
 'aiges.examples.stream.mmocr',
 'aiges.examples.stream.mock',
 'aiges.gradio_util',
 'aiges.protocol',
 'aiges.schema',
 'aiges.schema.utils',
 'aiges.test_data',
 'aiges.utils',
 'aiges.ws',
 'aiges.ws.tests']

package_data = \
{'': ['*'], 'aiges': ['tpls/*']}

install_requires = \
['Flask==2.2.5',
 'flask_restx>=1.0.0',
 'gradio>=3.0',
 'grpcio-health-checking>=1.50.0',
 'grpcio-tools>=1.50.0',
 'grpcio>=1.50.0',
 'jinja2>=2.0',
 'jsonref>=1.0.0',
 'plumbum>=1.7.0',
 'protobuf>=3.19',
 'pydantic==1.10.2']

setup_kwargs = {
    'name': 'aiges',
    'version': '0.12.1',
    'description': "A module for test aiges's python wrapper.py",
    'long_description': None,
    'author': 'maybaby',
    'author_email': 'ybyang7@iflytek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
