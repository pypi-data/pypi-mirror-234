# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mesh',
 'mesh.asm',
 'mesh.boost',
 'mesh.cause',
 'mesh.codec',
 'mesh.context',
 'mesh.environ',
 'mesh.examples',
 'mesh.grpx',
 'mesh.http',
 'mesh.ioc',
 'mesh.kinds',
 'mesh.log',
 'mesh.macro',
 'mesh.metrics',
 'mesh.mpc',
 'mesh.prsim',
 'mesh.runtime',
 'mesh.schema',
 'mesh.system',
 'mesh.test',
 'mesh.test.boost',
 'mesh.test.codec',
 'mesh.test.grpx',
 'mesh.test.ioc',
 'mesh.test.macro',
 'mesh.test.metrics',
 'mesh.test.mpc',
 'mesh.test.prsim',
 'mesh.test.tool',
 'mesh.tool']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.43.0,<2.0.0', 'protobuf>=3.14.0,<4.0.0']

setup_kwargs = {
    'name': 'daas',
    'version': '0.0.7',
    'description': 'A lightweight, distributed, relational network architecture for MPC.',
    'long_description': '# DaaS\n\n[![Build Status](https://travis-ci.org/ducesoft/babel.svg?branch=master)](https://travis-ci.org/ducesoft/babel)\n[![Financial Contributors on Open Collective](https://opencollective.com/babel/all/badge.svg?label=financial+contributors)](https://opencollective.com/babel) [![codecov](https://codecov.io/gh/babel/babel/branch/master/graph/badge.svg)](https://codecov.io/gh/babel/babel)\n![license](https://img.shields.io/github/license/ducesoft/babel.svg)\n\n中文版 [README](README_CN.md)\n\n## Introduction\n\nMesh is a standard implementation for [Private Transmission Protocol](Specifications.md) specification.\n\nMesh Python develop kits base on Python3.6. Recommend use [poetry](https://github.com/python-poetry/poetry) to manage\ndependencies.\n\n## Features\n\nAs an open source Internet of Data infrastructure develop kits, Mesh has the following core functions:\n\n* Minimal kernel with SPI plugin architecture, everything is replacement.\n* Support full stack of service mesh architecture.\n* Support full stack of service oriented architecture.\n* Support transport with TCP, HTTP, or other RPC protocols.\n* Support rich routing features.\n* Support reliable upstream management and load balancing capabilities.\n* Support network and protocol layer observability.\n* Support mTLS and protocols on TLS.\n* Support rich extension mechanism to provide highly customizable expansion capabilities.\n* Support process smooth upgrade.\n\n## Get Started\n\n```bash\npoetry add imesh\n```\n\nor\n\n```bash\npip install imesh\n```\n\n### RPC\n\nDeclared rpc interface Facade.\n\n```python\n\nfrom abc import ABC, abstractmethod\n\nfrom mesh import spi, mpi\n\n\n@spi("mesh")\nclass Tokenizer(ABC):\n\n    @abstractmethod\n    @mpi("mesh.trust.apply")\n    def apply(self, kind: str, duration: int) -> str:\n        """\n        Apply a node token.\n        :param kind:\n        :param duration:\n        :return:\n        """\n        pass\n\n    @abstractmethod\n    @mpi("mesh.trust.verify")\n    def verify(self, token: str) -> bool:\n        """\n        Verify some token verifiable.\n        :param token:\n        :return:\n        """\n        pass\n```\n\nDeclared rpc service Implement.\n\n```python\n\nfrom mesh import mps, Tokenizer\n\n\n@mps\nclass MeshTokenizer(Tokenizer):\n\n    def apply(self, kind: str, duration: int) -> str:\n        return "foo"\n\n    def verify(self, token: str) -> bool:\n        return True\n```\n\nRemote reference procedure call.\n\n```python\n\nfrom mesh import mpi, Tokenizer\n\n\nclass Component:\n\n    @mpi\n    def tokenizer(self) -> Tokenizer:\n        pass\n\n    def invoke(self) -> bool:\n        token = self.tokenizer().apply(\'PERMIT\', 1000 * 60 * 5)\n        return self.tokenizer().verify(token)\n\n\n```\n\n### Transport\n\nTransport is a full duplex communication stream implement.\n\n```python\nimport mesh\nfrom mesh import Mesh, log, ServiceLoader, Transport, Routable\nfrom mesh.prsim import Metadata\n\n\ndef main():\n    mesh.start()\n\n    transport = Routable.of(ServiceLoader.load(Transport).get("mesh"))\n    session = transport.with_address("10.99.1.33:570").local().open(\'session_id_008\', {\n        Metadata.MESH_VERSION.key(): \'\',\n        Metadata.MESH_TECH_PROVIDER_CODE.key(): \'LX\',\n        Metadata.MESH_TRACE_ID.key(): Mesh.context().get_trace_id(),\n        Metadata.MESH_TOKEN.key(): \'x\',\n        Metadata.MESH_SESSION_ID.key(): \'session_id_008\',\n        Metadata.MESH_TARGET_INST_ID.key(): \'JG0100000100000000\',\n    })\n    for index in range(100):\n        inbound = f"节点4发送给节点5报文{index}"\n        log.info(f"节点4发送:{inbound}")\n        session.push(inbound.encode(\'utf-8\'), {}, "topic")\n        outbound = session.pop(10000, "topic")\n        if outbound:\n            log.info(f"节点4接收:{outbound.decode(\'utf-8\')}")\n\n```\n',
    'author': 'coyzeng',
    'author_email': 'coyzeng@gmail.com',
    'maintainer': 'coyzeng',
    'maintainer_email': 'coyzeng@gmail.com',
    'url': 'https://github.com/jiumi/meio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
