# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'examples'}

packages = \
['sml']

package_data = \
{'': ['*']}

modules = \
['sml-mqtt-bridge', 'test_asyncio']
install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'async-timeout>=4.0',
 'bitstring>=3.1',
 'pyserial-asyncio>=0.6']

setup_kwargs = {
    'name': 'pysml',
    'version': '0.1.0',
    'description': 'Python library for EDL21 smart meters using Smart Message Language (SML)',
    'long_description': "# pysml\n\nPython library for EDL21 smart meters using Smart Message Language (SML)\n\nCan read SML data from physical serial ports, serial-over-tcp or HTTP.\n\nUsed by Home Assistant's EDL21 integration.\n\nThere's [example code](examples/sml-mqtt-bridge.py) for publishing OBIS values to an MQTT broker.\n",
    'author': 'Andreas Oberritter',
    'author_email': 'obi@saftware.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
