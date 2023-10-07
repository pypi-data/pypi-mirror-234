# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cofactr',
 'cofactr.schema',
 'cofactr.schema.flagship',
 'cofactr.schema.flagship_alts_v0',
 'cofactr.schema.flagship_cache_v0',
 'cofactr.schema.flagship_cache_v1',
 'cofactr.schema.flagship_cache_v2',
 'cofactr.schema.flagship_cache_v3',
 'cofactr.schema.flagship_cache_v4',
 'cofactr.schema.flagship_cache_v5',
 'cofactr.schema.flagship_cache_v6',
 'cofactr.schema.flagship_v2',
 'cofactr.schema.flagship_v3',
 'cofactr.schema.flagship_v4',
 'cofactr.schema.flagship_v5',
 'cofactr.schema.flagship_v6',
 'cofactr.schema.flagship_v7',
 'cofactr.schema.flagship_v8',
 'cofactr.schema.flagship_v9',
 'cofactr.schema.logistics',
 'cofactr.schema.logistics_v2',
 'cofactr.schema.logistics_v3',
 'cofactr.schema.logistics_v4',
 'cofactr.schema.price_solver_v0',
 'cofactr.schema.price_solver_v1',
 'cofactr.schema.price_solver_v10',
 'cofactr.schema.price_solver_v11',
 'cofactr.schema.price_solver_v2',
 'cofactr.schema.price_solver_v3',
 'cofactr.schema.price_solver_v4',
 'cofactr.schema.price_solver_v5',
 'cofactr.schema.price_solver_v6',
 'cofactr.schema.price_solver_v7',
 'cofactr.schema.price_solver_v8',
 'cofactr.schema.price_solver_v9']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'more-itertools>=9.0.0,<10.0.0',
 'tenacity>=8.1.0,<9.0.0',
 'typing-extensions>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'cofactr',
    'version': '5.36.0',
    'description': 'Client library for accessing Cofactr data.',
    'long_description': '# Cofactr\n\nPython client library for accessing Cofactr.\n\n## Example\n\n```python\nfrom typing import List\nfrom cofactr.graph import GraphAPI\n\n# Flagship is the default schema.\nfrom cofactr.schema.flagship.part import Part\n\ngraph = GraphAPI(client_id=..., api_key=...)\n\npart_res = graph.get_product(id="IM60640MOX6H")\npart: Part = part_res["data"]\n\nparts_res = graph.get_products(query="esp32")\nparts: List[Part] = parts_res["data"]\n```\n',
    'author': 'Joseph Sayad',
    'author_email': 'joseph@cofactr.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Cofactr/cofactr-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
