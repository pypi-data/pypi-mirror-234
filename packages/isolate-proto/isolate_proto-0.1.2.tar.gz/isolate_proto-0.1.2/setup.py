# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['isolate_proto', 'isolate_proto.health']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.49', 'isolate[build]>=0.12.2,<1.0', 'protobuf']

setup_kwargs = {
    'name': 'isolate-proto',
    'version': '0.1.2',
    'description': '(internal) gRPC definitions for Isolate Cloud',
    'long_description': '# gRPC definitions\n\nFor regenerating definitions:\n\n```\n$ cd projects/isolate_proto\n$ python ../../tools/regen_grpc.py src/isolate_proto/controller.proto <isolate version>\n$ pre-commit run --all-files\n```\n\nThe `<isolate version>` argument needs to be a [tag from the isolate Github project](https://github.com/fal-ai/isolate/tags) minus the leading `v`.\n',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
