# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['danbi',
 'danbi.analysis',
 'danbi.database',
 'danbi.dataprocess',
 'danbi.extends',
 'danbi.extends.bibokeh',
 'danbi.extends.bipandas',
 'danbi.extends.biray',
 'danbi.extends.bitensorflow',
 'danbi.extlib',
 'danbi.gym',
 'danbi.mapping',
 'danbi.plugable',
 'danbi.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'danbi',
    'version': '0.2.173',
    'description': 'python utility library',
    'long_description': '# danbi\n[![license]](/LICENSE)\n[![pypi]](https://pypi.org/project/danbi/)\n[![pyversions]](http://pypi.python.org/pypi/danbi)\n[![Downloads](https://pepy.tech/badge/danbi)](https://pepy.tech/project/danbi)\n\n---\n\ndanbi is python utility library.\n\n## Installation\n\n```python\npip install danbi\n```\n\n',
    'author': 'nockchun',
    'author_email': 'nockchun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nockchun/danbi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
