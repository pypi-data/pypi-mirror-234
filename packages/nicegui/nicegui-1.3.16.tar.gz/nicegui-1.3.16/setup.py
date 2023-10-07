# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nicegui',
 'nicegui.elements',
 'nicegui.elements.mixins',
 'nicegui.functions',
 'nicegui.json',
 'nicegui.tailwind_types']

package_data = \
{'': ['*'],
 'nicegui': ['static/*',
             'static/fonts/*',
             'static/lang/*',
             'static/utils/*',
             'templates/*'],
 'nicegui.elements': ['lib/aggrid/*',
                      'lib/echarts/*',
                      'lib/highcharts/*',
                      'lib/highcharts/modules/*',
                      'lib/mermaid/*',
                      'lib/nipplejs/*',
                      'lib/plotly/*',
                      'lib/three/*',
                      'lib/three/modules/*',
                      'lib/tween/*',
                      'lib/vanilla-jsoneditor/*']}

install_requires = \
['Pygments>=2.15.1,<3.0.0',
 'aiofiles>=23.1.0,<24.0.0',
 'aiohttp>=3.8.5,<4.0.0',
 'fastapi-socketio>=0.0.10,<0.0.11',
 'fastapi>=0.92,<1.0.0',
 'httpx>=0.24.1,<0.25.0',
 'itsdangerous>=2.1.2,<3.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'markdown2>=2.4.7,<3.0.0',
 'python-multipart>=0.0.6,<0.0.7',
 'typing-extensions>=3.10.0',
 'uvicorn[standard]>=0.22.0,<0.23.0',
 'vbuild>=0.8.2',
 'watchfiles>=0.18.1,<1.0.0']

extras_require = \
{':platform_machine != "i386" and platform_machine != "i686"': ['orjson>=3.8.6,<4.0.0'],
 'matplotlib': ['matplotlib>=3.5.0,<4.0.0'],
 'native': ['pywebview>=4.0.2,<5.0.0'],
 'netifaces': ['netifaces>=0.11.0,<0.12.0'],
 'plotly': ['plotly>=5.13.0,<6.0.0']}

setup_kwargs = {
    'name': 'nicegui',
    'version': '1.3.16',
    'description': 'Create web-based user interfaces with Python. The nice way.',
    'long_description': '<a href="http://nicegui.io/#about">\n  <img src="https://raw.githubusercontent.com/zauberzeug/nicegui/main/sceenshots/ui-elements-narrow.png"\n    width="200" align="right" alt="Try online!" />\n</a>\n\n# NiceGUI\n\nNiceGUI is an easy-to-use, Python-based UI framework, which shows up in your web browser.\nYou can create buttons, dialogs, Markdown, 3D scenes, plots and much more.\n\nIt is great for micro web apps, dashboards, robotics projects, smart home solutions and similar use cases.\nYou can also use it in development, for example when tweaking/configuring a machine learning algorithm or tuning motor controllers.\n\nNiceGUI is available as [PyPI package](https://pypi.org/project/nicegui/), [Docker image](https://hub.docker.com/r/zauberzeug/nicegui) and on [conda-forge](https://anaconda.org/conda-forge/nicegui) as well as [GitHub](https://github.com/zauberzeug/nicegui).\n\n[![PyPI](https://img.shields.io/pypi/v/nicegui?color=dark-green)](https://pypi.org/project/nicegui/)\n[![PyPI downloads](https://img.shields.io/pypi/dm/nicegui?color=dark-green)](https://pypi.org/project/nicegui/)\n[![Conda version](https://img.shields.io/conda/v/conda-forge/nicegui?color=green&label=conda-forge)](https://anaconda.org/conda-forge/nicegui)\n[![Conda downloads](https://img.shields.io/conda/dn/conda-forge/nicegui?color=green&label=downloads)](https://anaconda.org/conda-forge/nicegui)\n[![Docker pulls](https://img.shields.io/docker/pulls/zauberzeug/nicegui)](https://hub.docker.com/r/zauberzeug/nicegui)<br />\n[![GitHub license](https://img.shields.io/github/license/zauberzeug/nicegui?color=orange)](https://github.com/zauberzeug/nicegui/blob/main/LICENSE)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/graphs/commit-activity)\n[![GitHub issues](https://img.shields.io/github/issues/zauberzeug/nicegui?color=blue)](https://github.com/zauberzeug/nicegui/issues)\n[![GitHub forks](https://img.shields.io/github/forks/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/network)\n[![GitHub stars](https://img.shields.io/github/stars/zauberzeug/nicegui)](https://github.com/zauberzeug/nicegui/stargazers)\n\n## Features\n\n- browser-based graphical user interface\n- implicit reload on code change\n- acts as webserver (accessed by the browser) or in native mode (eg. desktop window)\n- standard GUI elements like label, button, checkbox, switch, slider, input, file upload, ...\n- simple grouping with rows, columns, cards and dialogs\n- general-purpose HTML and Markdown elements\n- powerful high-level elements to\n  - plot graphs and charts,\n  - render 3D scenes,\n  - get steering events via virtual joysticks\n  - annotate and overlay images\n  - interact with tables\n  - navigate foldable tree structures\n- built-in timer to refresh data in intervals (even every 10 ms)\n- straight-forward data binding and refreshable functions to write even less code\n- notifications, dialogs and menus to provide state of the art user interaction\n- shared and individual web pages\n- easy-to-use per-user and general persistence\n- ability to add custom routes and data responses\n- capture keyboard input for global shortcuts etc.\n- customize look by defining primary, secondary and accent colors\n- live-cycle events and session data\n- runs in Jupyter Notebooks and allows Python\'s interactive mode\n- auto-complete support for Tailwind CSS\n- SVG, Base64 and emoji favicon support\n\n## Installation\n\n```bash\npython3 -m pip install nicegui\n```\n\n## Usage\n\nWrite your nice GUI in a file `main.py`:\n\n```python\nfrom nicegui import ui\n\nui.label(\'Hello NiceGUI!\')\nui.button(\'BUTTON\', on_click=lambda: ui.notify(\'button was pressed\'))\n\nui.run()\n```\n\nLaunch it with:\n\n```bash\npython3 main.py\n```\n\nThe GUI is now available through http://localhost:8080/ in your browser.\nNote: NiceGUI will automatically reload the page when you modify the code.\n\n## Documentation and Examples\n\nThe documentation is hosted at [https://nicegui.io/documentation](https://nicegui.io/documentation) and provides plenty of live demos.\nThe whole content of [https://nicegui.io](https://nicegui.io) is [implemented with NiceGUI itself](https://github.com/zauberzeug/nicegui/blob/main/main.py).\n\nYou may also have a look at our [in-depth examples](https://github.com/zauberzeug/nicegui/tree/main/examples) of what you can do with NiceGUI.\nIn our wiki we have a list of great [NiceGUI projects from the community](https://github.com/zauberzeug/nicegui/wiki#community-projects), a section with [Tutorials](https://github.com/zauberzeug/nicegui/wiki#tutorials), a growing list of [FAQs](https://github.com/zauberzeug/nicegui/wiki/FAQs) and [some strategies for using ChatGPT / LLMs to get help about NiceGUI](https://github.com/zauberzeug/nicegui/wiki#chatgpt).\n\n## Why?\n\nWe at [Zauberzeug](https://zauberzeug.com) like [Streamlit](https://streamlit.io/)\nbut find it does [too much magic](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651) when it comes to state handling.\nIn search for an alternative nice library to write simple graphical user interfaces in Python we discovered [JustPy](https://justpy.io/).\nAlthough we liked the approach, it is too "low-level HTML" for our daily usage.\nBut it inspired us to use [Vue](https://vuejs.org/) and [Quasar](https://quasar.dev/) for the frontend.\n\nWe have built on top of [FastAPI](https://fastapi.tiangolo.com/),\nwhich itself is based on the ASGI framework [Starlette](https://www.starlette.io/)\nand the ASGI webserver [Uvicorn](https://www.uvicorn.org/)\nbecause of their great performance and ease of use.\n\n## Contributing\n\nThank you for your interest in contributing to NiceGUI! We are thrilled to have you on board and appreciate your efforts to make this project even better.\n\nAs a growing open-source project, we understand that it takes a community effort to achieve our goals. That\'s why we welcome all kinds of contributions, no matter how small or big they are. Whether it\'s adding new features, fixing bugs, improving documentation, or suggesting new ideas, we believe that every contribution counts and adds value to our project.\n\nWe have provided a detailed guide on how to contribute to NiceGUI in our [CONTRIBUTING.md](https://github.com/zauberzeug/nicegui/blob/main/CONTRIBUTING.md) file. We encourage you to read it carefully before making any contributions to ensure that your work aligns with the project\'s goals and standards.\n\nIf you have any questions or need help with anything, please don\'t hesitate to reach out to us. We are always here to support and guide you through the contribution process.\n\n### Included Web Dependencies\n\nSee [DEPENDENCIES.md](https://github.com/zauberzeug/nicegui/blob/main/DEPENDENCIES.md) for a list of web frameworks NiceGUI depends on.\n',
    'author': 'Zauberzeug GmbH',
    'author_email': 'info@zauberzeug.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zauberzeug/nicegui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
