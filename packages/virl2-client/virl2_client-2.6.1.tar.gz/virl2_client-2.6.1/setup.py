# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virl2_client', 'virl2_client.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.24.0,<0.25.0', 'urllib3>=1,<2']

extras_require = \
{'docs': ['sphinx_rtd_theme>=1,<2', 'sphinx>=6,<7'],
 'events': ['aiohttp'],
 'pyats': ['pyats>=23,<24']}

setup_kwargs = {
    'name': 'virl2-client',
    'version': '2.6.1',
    'description': 'VIRL2 Client Library',
    'long_description': '[![CI](https://github.com/CiscoDevNet/virl2-client/actions/workflows/main.yml/badge.svg)](https://github.com/CiscoDevNet/virl2-client/actions/workflows/main.yml)\n\n# VIRL 2 Client Library\n\n> **Note:** The product has been renamed from *VIRL* to *Cisco Modeling Labs* /\n> CML 2.  References to VIRL still exist in the product documentation and within\n> code or examples.\n>\n> The name of the package itself has not been changed.  Throughout the\n> documentation it is referred to as "virl2_client",  "Python Client Library" or\n> "PCL".\n\n## Introduction\n\nThis is the client library for the *Cisco Modeling Labs* Platform\n(`virl2_client`). It provides a Python package to programmatically create,\nedit, delete and control network simulations on a CML 2 controller.\n\nIt is a pure Python implementation that requires Python 3. We\'ve tested and\nwritten the package with Python 3.8.10.\n\nThe status of the package can be considered **stable**.  Issues with the\nsoftware should be raised via the [GitHub issue\ntracker](https://github.com/CiscoDevNet/virl2-client/issues).\n\n## Use Case Description\n\nThe client library provides a convenient interface to control the life-cycle of\na network simulation. This can be used for automation scripts directly in\nPython but also for third party integrations / plugins which need to integrate\nwith a simulated network. Examples already existing are an [Ansible\nplugin](https://github.com/CiscoDevNet/ansible-virl).\n\n## Installation\n\nThe package comes in form of a wheel that is downloadable from the CML\n2 controller. The package can be installed either from PyPI using\n\n    pip3 install virl2_client\n\nIf you want to interact with devices via the client library, you need to\nalso install the pyATS library. This can be achieved in one go using\n\n```\npip3 install "virl2_client[pyats]"\n```\n\nNote that this does *not* pull in the full pyATS package... See below how that is achieved.\n\nor, alternatively, the version that is bundled with the CML 2 controller can\nbe downloaded to the local filesystem and then directly installed via\n\n    pip3 install ./virl2_client-*.whl\n\nThe bundled version is available on the index site of the docs when viewed\ndirectly on the CML 2 controller.\n\nEnsure to replace and/or use the correct file name, replacing the wildcard with the\nproper version/build information. For example\n\n    pip3 install virl2_client-2.0.0b10-py3-none-any.whl\n\nWe recommend the use of a virtual environment for installation.\n\nIf you require the full version of the pyATS library including things like Genie\nthen you need to do this in a subsequent step like shown here:\n\n    pip3 install "pyats[full]"\n\n> **IMPORTANT**: The version of the Python client library  must be compatible\n> with the version of the controller.  If you are running an older controller\n> version then it\'s likely that the latest client library version from PyPI can\n> **not** be used.  In this case, you need to either use the version available\n> from the controller itself or by specifying a version constraint.\n>\n> Example: When on a controller version 2.2.x, then you\'d need to install with\n> `pip3 install "virl2-client<2.3.0"`. This will ensure that the version\n> installed is compatible with 2.2.x.\n\n## Usage\n\nThe package itself is fairly well documented using *docstrings*. In addition, the\ndocumentation is available in HTML format on the controller itself, via the\n"Tools -> Client Library" menu.\n\n## Compatibility\n\nThis package and the used API is specific to CML 2. It is not\nbackwards compatible with VIRL 1.x and therefore can not be used with VIRL\n1.x. If you are looking for a convenient tool to interface with the VIRL 1 API\nthen the [CML Utils tool](https://github.com/CiscoDevNet/virlutils) is\nrecommended.\n\n## Known Issues\n\nThere are no major known issues at this point. See the comment in the *Introduction*\nsection.  Also, see the *Issues* section in GitHub to learn about known issues or raise new ones, if needed.  Also see [CHANGES](CHANGES.md).\n\n## Getting Help\n\nIf you have questions, concerns, bug reports, etc., please create an issue\nagainst the [repository on\nGitHub](https://github.com/CiscoDevNet/virl2-client/)\n\n## Getting Involved\n\nWe welcome contributions. Whether you fixed a bug, added a new feature or\ncorrected a typo, all contributions are welcome. General instructions on how to\ncontribute can be found in the [CONTRIBUTING](CONTRIBUTING.md) file.\n\n## Licensing Info\n\nThis code is licensed under the Apache 2.0 License. See [LICENSE](LICENSE) for\ndetails.\n\n## References\n\nThis package is part of the CML 2 Network Simulation platform. For details, go\nto <https://developer.cisco.com/modeling-labs>. Additional documentation for the\nproduct is available at <https://developer.cisco.com/docs/modeling-labs>\n',
    'author': 'Simon Knight',
    'author_email': 'simknigh@cisco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ciscodevnet/virl2-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
