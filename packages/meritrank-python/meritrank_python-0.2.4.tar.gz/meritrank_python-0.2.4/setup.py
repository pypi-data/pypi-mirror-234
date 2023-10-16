# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meritrank_python']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.8.8,<3.0.0']

setup_kwargs = {
    'name': 'meritrank-python',
    'version': '0.2.4',
    'description': 'MeritRank decentralized, sybil-resistant, personalized ranking algorithm library',
    'long_description': 'Copyright: Vadim Bulavintsev (GPL v2)\n\n# MeritRank Python implementation\n\nThis repository contains the Python implementation for the incremental version of the MeritRank \nscoring system (which is inspired by personalized PageRank).\n\n\n## Usage example\n```python\nfrom meritrank_python.rank import IncrementalMeritRank\n\npr = IncrementalMeritRank()\n\npr.add_edge(0, 1, )\npr.add_edge(0, 2, weight=0.5)\npr.add_edge(1, 2, weight=2.0)\n\n# Initalize calculating rank from the standpoint of node "0"\npr.calculate(0)\n\n# Get the score for node "1" from the standpoint of the node "0" \nprint(pr.get_node_score(0, 1))\n\n# Add another edge: note that the scores are automatically recalculated\npr.add_edge(2, 1, weight=3.0)\nprint(pr.get_node_score(0, 1))\n\n```\n\n## Known issues and limitations\n* The bookkeeping algorithm for the incremental \naddition-deletion of edges is pretty complex.  \nInitial tests show its results are equivalent to non-incremental version,\nat least for all possible transitions between all possible meaningful 3- and 4-nodes graphs.\nNonetheless, it is hard to predict how the thing will work in real-life scenarios.\n',
    'author': 'V.G. Bulavintsev',
    'author_email': 'golem.md@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ichorid/meritrank-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
