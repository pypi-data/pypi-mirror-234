# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['craft_ai_sdk']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0', 'StrEnum>=0.4.9,<0.5.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['bump-version = scripts.scripts:bump_version',
                     'format = scripts.scripts:format',
                     'lint = scripts.scripts:lint',
                     'pdfdoc = scripts.scripts:generate_docs_in_pdf',
                     'reformat = scripts.scripts:reformat',
                     'rstdoc = scripts.scripts:generate_docs_in_rst',
                     'test = scripts.scripts:test',
                     'test-base = scripts.scripts:test_base',
                     'test-platform = scripts.scripts:test_platform',
                     'update-testrunner-token = '
                     'scripts.scripts:update_testrunner_token']}

setup_kwargs = {
    'name': 'craft-ai-sdk',
    'version': '0.28.0rc1',
    'description': 'Craft AI MLOps platform SDK',
    'long_description': '# Craft AI Python SDK\n\nThis Python SDK lets you interact with Craft AI MLOps Platform.\n\n## Installation\nThis project relies on **Python 3.8+**. Once a supported version of Python is installed, you can install `craft-ai-sdk` from PyPI with:\n\n```console\npip install craft-ai-sdk\n```\n\n## Basic usage\nYou can configure the SDK by instantiating the `CraftAiSdk` class in this way:\n\n```python\nfrom craft_ai_sdk import CraftAiSdk\n\nCRAFT_AI_SDK_TOKEN =  # your access key obtained from your settings page\nCRAFT_AI_ENVIRONMENT_URL =  # url to your environment\n\nsdk = CraftAiSdk(sdk_token=CRAFT_AI_SDK_TOKEN, environment_url=CRAFT_AI_ENVIRONMENT_URL)\n```\n\nIf using the SDK in interactive mode, some additional feedbacks will be printed. You can force disable or enable those logs by either\n* Setting the `verbose_log` SDK parameter\n* Or setting the `SDK_VERBOSE_LOG` env var\n',
    'author': 'Craft AI',
    'author_email': 'contact@craft.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.craft.ai/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
