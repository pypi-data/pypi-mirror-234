# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ensure_import']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['prepare = ensure_import.prepare:run']}

setup_kwargs = {
    'name': 'ensure-import',
    'version': '0.3.4',
    'description': 'Auto install third part packages by pip into virtual environment when import error.',
    'long_description': "# ensure_import\n\n[![LatestVersionInPypi](https://img.shields.io/pypi/v/ensure_import.svg?style=for-the-badge)](https://pypi.python.org/pypi/ensure_import)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge)](https://github.com/pre-commit/pre-commit)\n\nAuto install third part packages by pip into virtual environment when import error.\n\n## Install\n```bash\npip install ensure_import\n```\n\n## Usage\n- Simple case that package name is module name\n```py\nfrom ensure_import import EnsureImport as _EI\n\nwhile _ei := _EI():\n    with _ei:\n        import uvicorn\n        from fastapi import FastAPI\n```\n- Package name is difference from module name\n```py\nwhile _ei := _EI():\n    with _ei(dotenv='python-dotenv', odbc='pyodbc'):\n        import numpy as np\n        import uvicorn\n        import odbc  # who's package name is `pyodbc`\n        from fastapi import FastAPI\n        # package name of dotenv is `python-dotenv`\n        from dotenv import load_dotenv\n```\n- Supply module path\n```py\nwhile _ei := _EI('..'):\n    with _ei:\n        import gunicorn\n        import uvicorn\n```\nThis is equal to:\n```py\ntry:\n    import gunicorn\n    import uvicorn\nexcept ImportError:\n    import sys\n    sys.path.append('..')\n\n    import gunicorn\n    import uvicorn\n```\n",
    'author': 'Waket Zheng',
    'author_email': 'waketzheng@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/waketzheng/ensure_import',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
