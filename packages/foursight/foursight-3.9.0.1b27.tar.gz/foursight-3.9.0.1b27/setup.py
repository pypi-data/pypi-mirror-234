# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chalicelib_fourfront',
 'chalicelib_fourfront.checks',
 'chalicelib_fourfront.checks.helpers']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'MarkupSafe>=2.1.3,<3.0.0',
 'PyJWT>=2.5.0,<3.0.0',
 'benchmark-4dn>=0.5.17,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'dcicutils==7.12.0.2b9',
 'elasticsearch-dsl>=7.0.0,<8.0.0',
 'elasticsearch==7.13.4',
 'foursight-core==4.5.0.3b27',
 'geocoder==1.38.1',
 'gitpython>=3.1.2,<4.0.0',
 'google-analytics-data>=0.17.1,<0.18.0',
 'gspread>=3.6.0',
 'oauth2client>=4.1.3',
 'pytest-redis>=3.0.2,<4.0.0',
 'pytest>=7.4.2,<8.0.0',
 'pytz>=2020.1,<2021.0',
 'tibanna-ff==2.0.1.1b10']

entry_points = \
{'console_scripts': ['decrypt-accounts-file = '
                     'foursight_core.scripts.decrypt_accounts_file:main',
                     'encrypt-accounts-file = '
                     'foursight_core.scripts.encrypt_accounts_file:main',
                     'publish-to-pypi = '
                     'dcicutils.scripts.publish_to_pypi:main']}

setup_kwargs = {
    'name': 'foursight',
    'version': '3.9.0.1b27',
    'description': 'Serverless Chalice Application for Monitoring',
    'long_description': 'None',
    'author': '4DN-DCIC Team',
    'author_email': 'support@4dnucleome.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
