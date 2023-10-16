# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pipen_lock']
install_requires = \
['filelock>=3,<4', 'pipen>=0.11,<0.12']

entry_points = \
{'pipen': ['lock = pipen_lock:pipen_lock_plugin']}

setup_kwargs = {
    'name': 'pipen-lock',
    'version': '0.4.0',
    'description': 'Process lock for pipen to prevent multiple runs at the same time',
    'long_description': '# pipen-lock\n\nProcess lock for pipen to prevent multiple runs at the same time\n\n## Installation\n\n```bash\npip install -U pipen-lock\n```\n\n## Enable/Disable\n\nThe plugin is enabled by default. To disable it, either uninstall it or:\n\n```python\nfrom pipen import Proc, Pipen\n\n# process definition\n\nclass MyPipeline(Pipen):\n    plugins = ["no:lock"]\n\n```\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
