# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pipen_dry']
install_requires = \
['pipen>=0.11,<0.12']

entry_points = \
{'pipen': ['dry = pipen_dry:PipenDry'],
 'pipen_sched': ['dry = pipen_dry:PipenDryScheduler']}

setup_kwargs = {
    'name': 'pipen-dry',
    'version': '0.7.0',
    'description': 'Dry runner for pipen pipelines',
    'long_description': '# pipen-dry\n\nDry runner for [pipen][1]\n\nIt is useful to quickly check if there are misconfigurations for your pipeline without actually running it.\n\n## Install\n\n```shell\npip install -U pipen-dry\n```\n\n## Usage\n\n- Use it for process\n\n    ```python\n    class P1(Proc):\n        scheduler = "dry"\n    ```\n\n- Use it for pipeline\n\n    ```python\n    Pipen(scheduler="dry", ...)\n    ```\n\n[1]: https://github.com/pwwang/pipen\n',
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
