# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdpd']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.1.1,<3.0.0']

setup_kwargs = {
    'name': 'mdpd',
    'version': '0.1.0',
    'description': 'a simpler tool for convert markdown table to pandas',
    'long_description': '# mdpd\n`mdpd` is a simpler tool for convert markdown table to pandas.\nThis tool is a lightweight tool for testing a code, so note that we are not validating the user\'s input.\n\n## usage\n\n```python\n# pip install mdpd\nimport mdpd\n\ndf = mdpd.from_md("""\n+------------+-------+\n| id         | score |\n+------------+-------+\n| 1          | 15    |\n| 2          | 11    |\n| 3          | 11    |\n| 4          | 20    |\n+------------+-------+\n""")\n\nprint(df)\n#   id score\n# 0  1    15\n# 1  2    11\n# 2  3    11\n# 3  4    20\n```\n\n\n## accepted table patterns\n\n```markdown\n| Syntax    | Description |\n| --------- | ----------- |\n| Header    | Title       |\n| Paragraph | Text        |\n```\n\n```markdown\n+------------+-------------+\n| Syntax     | Description |\n+------------+-------------+\n| Header     | Title       |\n| Paragraph  | Text        |\n+------------+-------------+\n```\n\n```markdown\n| Syntax    | Description |\n| :-------- | ----------: |\n| Header    | Title       |\n| Paragraph | Text        |\n```\n\n## contribute\nIf you have suggestions for features or improvements to the code, please feel free to create an issue or PR.\n',
    'author': 'kyoto7250',
    'author_email': '50972773+kyoto7250@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyoto7250/mdpd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
