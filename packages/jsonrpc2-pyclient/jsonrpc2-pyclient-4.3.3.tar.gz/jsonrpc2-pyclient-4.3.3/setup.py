# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonrpc2pyclient']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.25.0,<0.26.0',
 'jsonrpc2-objects>=3.0.0,<4.0.0',
 'websockets>=11.0.3,<12.0.0']

setup_kwargs = {
    'name': 'jsonrpc2-pyclient',
    'version': '4.3.3',
    'description': 'Python JSON-RPC 2.0 client library.',
    'long_description': '<div align="center">\n<!-- Title: -->\n  <h1>JSON RPC PyClient</h1>\n<!-- Labels: -->\n  <!-- First row: -->\n  <img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg"\n   height="20"\n   alt="License: AGPL v3">\n  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"\n   height="20"\n   alt="Code style: black">\n  <img src="https://img.shields.io/pypi/v/jsonrpc2-pyclient.svg"\n   height="20"\n   alt="PyPI version">\n  <a href="https://gitlab.com/mburkard/jsonrpc-pyclient/-/blob/main/CONTRIBUTING.md">\n    <img src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=00b250"\n     height="20"\n     alt="Contributions Welcome">\n  </a>\n  <h3>A library for creating JSON RPC 2.0 clients in Python with async support</h3>\n</div>\n\n## Install\n\n```shell\npoetry add jsonrpc2-pyclient\n```\n\n```shell\npip install jsonrpc2-pyclient\n```\n\n## Example\n\nExample of the client decorator implementing rpc methods from reading\nmethod signatures.\n\n```python\nimport asyncio\n\nfrom pydantic import BaseModel\n\nfrom jsonrpc2pyclient.decorator import rpc_client\nfrom jsonrpc2pyclient.httpclient import AsyncRPCHTTPClient\n\ntransport = AsyncRPCHTTPClient("http://127.0.0.1:8000/api/v1")\n\n\nclass Vector3(BaseModel):\n    x: float = 1.0\n    y: float = 1.0\n    z: float = 1.0\n\n\n@rpc_client(transport=transport)\nclass TestClient:\n    async def add(self, a: int, b: int) -> int: ...\n    async def get_distance(self, a: Vector3, b: Vector3) -> Vector3: ...\n\n\nasync def main() -> None:\n    client = TestClient()\n    assert await client.add(3, 4) == 7\n    assert await client.get_distance(Vector3(), Vector3()) == Vector3(x=0, y=0, z=0)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n### RPCClient Abstract Class\n\nJSON-RPC 2.0 is transport agnostic. This library provides an abstract\nclass that can be extended to create clients for different transports.\n\n### Transports\n\nTo make client for a transport, extend the `RPCClient` class and\nimplement the `_send_and_get_json` which takes a request as a str and is\nexpected to return a JSON-RPC 2.0 response as a str or byte string.\n`RPCClient` has a `call` method that uses this internally.\n\nA default HTTP and Websocket implementation is provided.\n\n### Usage\n\nThe `RPCClient` will handle forming requests and parsing responses.\nTo call a JSON-RPC 2.0 method with an implementation of `RPCClient`,\ncall the `call` method, passing it the name of the method to call and\nthe params.\n\nIf the response is JSON-RPC 2.0 result object, only the result will be\nreturned, none of the wrapper.\n\nIf the response is JSON-RPC 2.0 error response, and exception will be\nthrown for the error.\n\n```python\nfrom jsonrpc2pyclient.httpclient import RPCHTTPClient\nfrom jsonrpcobjects.errors import JSONRPCError\n\nclient = RPCHTTPClient("http://localhost:5000/api/v1/")\ntry:\n    res = client.call("divide", [0, 0])\n    print(f"JSON-RPC Result: {res}")\nexcept JSONRPCError as e:\n    print(f"JSON-RPC Error: {e}")\n```\n\n## Client Decorator\n\nThe `rpc_client` decorator can be used to quickly put together a client\nwith typed methods. When a class is decorated, each method defined in\nthat class will make RPC requests using the provided transport and parse\nthe result. The name of the method will be used in the RPC request.\n\nThe method body must end with `...` for the decorator to implement it.\n\n```python\ntransport = RPCHTTPClient("http://127.0.0.1:8000/api/v1")\n\n@rpc_client(transport=transport)\nclass TestClient:\n    def add(self, a: int, b: int) -> int: ...\n\n\nclient = TestClient()\nassert client.add(3, 4) == 7\n```\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/jsonrpc2-pyclient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
