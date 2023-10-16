# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_diagram']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.20,<0.21', 'pipen>=0.11,<0.12']

entry_points = \
{'pipen': ['diagram = pipen_diagram:PipenDiagram']}

setup_kwargs = {
    'name': 'pipen-diagram',
    'version': '0.8.0',
    'description': 'Draw pipeline diagrams for pipen.',
    'long_description': '# pipen-diagram\n\nDraw pipeline diagrams for [pipen][1].\n\n## Features\n\n- Diagram theming\n- Hiding processes from diagram\n\n## Configurations\n\n- `diagram_theme`: The name of the theme to use, or a dict of a custom theme.\n  - See `pipen_diagram/diagram.py` for the a theme definition\n  - See [https://graphviz.org/][2] for theme items\n- `diagram_savedot`: Whhether to save the dot file (for debugging purpose)\n- `diagram_hide`: Process-level item, whether to hide current process from the diagram\n\n## Installation\n\n```shell\npip install -U pipen-diagram\n```\n\n## Enabling/Disabling the plugin\n\nThe plugin is registered via entrypoints. It\'s by default enabled. To disable it:\n`plugins=[..., "no:diagram"]`, or uninstall this plugin.\n\n## Usage\n\n`example.py`\n\n```python\nfrom pipen import Proc, Pipen, ProcGroup\n\n\nclass A(Proc):\n    """Process A"""\n    input = "a"\n\n\nclass B(Proc):\n    """Process B"""\n    requires = A\n    input = "b"\n    plugin_opts = {"diagram_hide": True}\n\n\nclass PG(ProcGroup):\n    """Process Group"""\n    @ProcGroup.add_proc\n    def c(self):\n        """Process C"""\n        class C(Proc):\n            input = "c"\n\n        return C\n\n    @ProcGroup.add_proc\n    def c1(self):\n        """Process C1"""\n        class C1(Proc):\n            requires = self.c\n            input = "c1"\n            plugin_opts = {"diagram_hide": True}\n\n        return C1\n\n    @ProcGroup.add_proc\n    def d(self):\n        """Process D"""\n        class D(Proc):\n            input = "d"\n            requires = self.c1\n\n        return D\n\n\npg = PG()\npg.c.requires = B\n\n\nclass E(Proc):\n    """Process E"""\n    input = "e1,e2"\n    requires = pg.d, A\n\n\nclass F(Proc):\n    """Process F"""\n    input = "f"\n    requires = E\n\n\nPipen("MyPipeline").set_start(A).run()\n# Dark theme\n# Pipen("MyPipeline", plugin_opts={"diagram_theme": "dark"}).set_start(A).run()\n```\n\nRunning `python example.py` will generate `MyPipeline-output/diagram.svg`:\n\n| Default theme | Dark theme | Fancy theme | Fancy dark theme |\n| ------------- | ---------- | ----------- | ---------------- |\n| ![diagram](./diagram.svg) | ![diagram_dark](./diagram_dark.svg) | ![diagram_fancy](./diagram_fancy.svg) | ![diagram_fancy_dark](./diagram_fancy_dark.svg) |\n\n[1]: https://github.com/pwwang/pipen\n[2]: https://graphviz.org/\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pwwang/pipen-diagram',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
