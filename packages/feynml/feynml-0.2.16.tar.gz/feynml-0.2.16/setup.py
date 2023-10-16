# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feynml', 'feynml.interface', 'feynml.interface.formcalc']

package_data = \
{'': ['*']}

install_requires = \
['cssselect',
 'cssutils',
 'deprecated',
 'deprecation',
 'particle',
 'smpl_doc>=1.1.3,<2.0.0',
 'smpl_io>=1.1.2,<2.0.0',
 'smpl_util',
 'xsdata[cli,lxml,soap]']

extras_require = \
{'interfaces': ['pyqgraf>=0.0.3', 'pyhepmc', 'pylhe']}

setup_kwargs = {
    'name': 'feynml',
    'version': '0.2.16',
    'description': 'Feynman diagram markup language',
    'long_description': '# FeynML\n\nFeynML from <https://feynml.hepforge.org/>\n\nFeynML is a project to develop an XML dialect for describing Feynman diagrams as used in quantum field theory calculations. The primary aim is to unambiguously describe the structure of a diagram in XML, giving a de facto representation for diagram structure which can be easily translated into another representation.\n\n[![PyPI version][pypi image]][pypi link] [![PyPI version][pypi versions]][pypi link]  ![downloads](https://img.shields.io/pypi/dm/feynml.svg)\n\n\n[![test][a t image]][a t link]     [![Coverage Status][c t i]][c t l] [![Codacy Badge][cc c i]][cc c l]  [![Codacy Badge][cc q i]][cc q l]  [![Documentation][rtd t i]][rtd t l]\n\n## Installation\n```sh\npip install [--user] feynml\n```\n\nor from cloned source:\n\n```sh\npoerty install --with docs --with dev\npoetry shell\n```\n\n## Documentation\n\n*   <https://pyfeyn2.readthedocs.io/en/stable/feynml/>\n*   <https://apn-pucky.github.io/pyfeyn2/feynml/index.html>\n\n## Related:\n\n*   <https://github.com/APN-Pucky/pyfeyn2>\n\n\n## Development\n\n\n### package/python structure:\n\n*   <https://mathspp.com/blog/how-to-create-a-python-package-in-2022>\n*   <https://www.brainsorting.com/posts/publish-a-package-on-pypi-using-poetry/>\n\n\n[pypi image]: https://badge.fury.io/py/feynml.svg\n[pypi link]: https://pypi.org/project/feynml/\n[pypi versions]: https://img.shields.io/pypi/pyversions/feynml.svg\n\n[a t link]: https://github.com/APN-Pucky/feynml/actions/workflows/test.yml\n[a t image]: https://github.com/APN-Pucky/feynml/actions/workflows/test.yml/badge.svg\n\n\n[cc q i]: https://app.codacy.com/project/badge/Grade/135bae47c6344ab0bfb180135ea1db44\n[cc q l]: https://www.codacy.com/gh/APN-Pucky/feynml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/feynml&amp;utm_campaign=Badge_Grade\n[cc c i]: https://app.codacy.com/project/badge/Coverage/135bae47c6344ab0bfb180135ea1db44\n[cc c l]: https://www.codacy.com/gh/APN-Pucky/feynml/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/feynml&utm_campaign=Badge_Coverage\n\n[c t l]: https://coveralls.io/github/APN-Pucky/feynml?branch=master\n[c t i]: https://coveralls.io/repos/github/APN-Pucky/feynml/badge.svg?branch=master\n\n[rtd t i]: https://readthedocs.org/projects/pyfeyn2/badge/?version=latest\n[rtd t l]: https://pyfeyn2.readthedocs.io/en/latest/?badge=latest\n',
    'author': 'Alexander Puck Neuwirth',
    'author_email': 'alexander@neuwirth-informatik.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/APN-Pucky/feynml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
