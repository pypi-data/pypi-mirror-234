# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ably',
 'ably.http',
 'ably.realtime',
 'ably.rest',
 'ably.scripts',
 'ably.sync',
 'ably.sync.http',
 'ably.sync.realtime',
 'ably.sync.rest',
 'ably.sync.scripts',
 'ably.sync.transport',
 'ably.sync.types',
 'ably.sync.util',
 'ably.transport',
 'ably.types',
 'ably.util']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.24.1,<0.25.0',
 'methoddispatch>=3.0.2,<4.0.0',
 'msgpack>=1.0.0,<2.0.0',
 'pyee>=9.0.4,<10.0.0',
 'websockets>=10.3,<11.0']

extras_require = \
{'crypto': ['pycryptodome'], 'oldcrypto': ['pycrypto>=2.6.1,<3.0.0']}

entry_points = \
{'console_scripts': ['unasync = ably.scripts.unasync:run']}

setup_kwargs = {
    'name': 'ably',
    'version': '2.0.2rc3',
    'description': 'Python REST and Realtime client library SDK for Ably realtime messaging service',
    'long_description': 'Official Ably Bindings for Python\n==================================\n\nA Python client library for Ably Realtime messaging.\n\n\nSetup\n-----\n\nYou can install this package by using the pip tool and installing:\n\n    pip install ably\n\n\nUsing Ably for Python\n---------------------\n\n- Sign up for Ably at https://ably.com/sign-up\n- Get usage examples at https://github.com/ably/ably-python\n- Visit https://ably.com/docs for a complete API reference and more examples\n',
    'author': 'Ably',
    'author_email': 'support@ably.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ably.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
