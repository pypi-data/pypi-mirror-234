# bibigo

**Python Template Generator.**



### Installation

----

**Use pipx!**

You can run Python application in isolated environment! (like `brew`, `apt`, `npx`)

```bash
user@host:~$ python -m pip install pipx
user@host:~$ python -m pipx install bibigo
```



### How to use

---
__(1) Create Empty Project w/ formatter and linter (for vscode)__

```bash
user@host:~$ mkdir my-settings
user@host:~$ cd my-settings
user@host:~/my-settings$ bibigo init settings .

╭──────────────────────────────────────────────────────────────────────────────────────╮
│ Settings for Project 'my-settings' is Ready.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

__(2) Create a pip installable python package template__

```bash
user@host:~$ mkdir my-package
user@host:~$ cd my-package
user@host:~/my-package$ bibigo init package .
? Project Name  my-package
? Author  Woojin Cho
? Author Email  woojin.cho@gmail.com
? Description  Test Template
? Long Description  file: README.md
? Keywords  python, test, template, for, installable, package
? License  MIT License
? Python Requires  >= 3.8
? Install Requires  click, pandas, numpy
? Your Private PyPI  http://my-private.pypi.me/simple
? Confirm Initializer  Yes

╭──────────────────────────────────────────────────────────────────────────────────────╮
│ Python project 'my-package' is ready.                                                │
│  - Build Package: 'python -m build', python package 'build' is required.             │
│  - Upload to PyPI: 'twine upload dist/*', python package 'twine is required.         │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```
