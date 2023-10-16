import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from ..utils import read, write, STATIC_DIR
from ..exceptions import CancelInit

console = Console(width=88)


################################################################
# init package
################################################################
def init_package(root):
    from InquirerPy import prompt

    # get project name from input
    fp = Path(root)
    project = fp.absolute().name

    # get private pypi url
    private_pypi = os.getenv("PIP_INDEX_URL") or ""

    # set setup configuration
    setup_conf = [
        {"type": "input", "name": "project", "default": project, "message": "Project Name"},
        {"type": "input", "name": "author", "message": "Author"},
        {"type": "input", "name": "author_email", "message": "Author Email"},
        {"type": "input", "name": "description", "message": "Description"},
        {"type": "input", "name": "long_description", "message": "Long Description"},
        {"type": "input", "name": "keywords", "message": "Keywords"},
        {"type": "input", "name": "license", "default": "MIT License", "message": "License"},
        {"type": "input", "name": "python_requires", "default": ">= 3.9", "message": "Python Requires"},
        {
            "type": "input",
            "name": "install_requires",
            "message": "Install Requires (e.g., pandas, numpy)",
            "filter": lambda x: [_.strip() for _ in x.split(",")],
        },
        {
            "type": "input",
            "name": "dependency_links",
            "default": private_pypi,
            "message": "Your Private PyPI",
        },
        {"type": "confirm", "name": "confirm", "message": "Confirm"},
    ]

    # user input
    conf = prompt(setup_conf)
    confirm = conf.pop("confirm")
    if not confirm:
        raise CancelInit

    # correct install requires
    if conf["install_requires"] is not None:
        TAB = "    "
        for default_package in ["click"]:
            if default_package not in conf["install_requires"]:
                conf["install_requires"].insert(0, default_package)
        conf["install_requires"] = f"\n{TAB}".join(conf["install_requires"])

    # update package_name (replace "-" to "_" from project)
    conf.update({"package_name": conf["project"].replace("-", "_")})

    # [WRITE FILES]
    # MANIFEST.in
    MANIFEST_IN_FILE = "MANIFEST.in"
    write(
        dst_fp=fp / MANIFEST_IN_FILE,
        content=read(MANIFEST_IN_FILE).format(**conf),
    )

    # pyproject.toml
    PYPROJECT_TOML_FILE = "pyproject.toml"
    write(
        dst_fp=fp / PYPROJECT_TOML_FILE,
        content=read(PYPROJECT_TOML_FILE).format(**conf),
    )

    # setup.cfg
    SETUP_CFG_FILE = "setup.cfg"
    write(
        dst_fp=fp / SETUP_CFG_FILE,
        content=read(SETUP_CFG_FILE).format(**conf),
    )

    # Dockerfile
    DOCKERFILE_FILE = "Dockerfile"
    write(
        dst_fp=fp / DOCKERFILE_FILE,
        content=read(DOCKERFILE_FILE),
    )

    # make src directory
    (fp / "src").mkdir(exist_ok=True)
    package_name = conf["package_name"]
    package_root = fp / "src" / package_name
    package_root.mkdir(exist_ok=True)

    # src/__init__.py
    INIT_PY_FILE = "__init__.py"
    write(
        dst_fp=package_root / INIT_PY_FILE,
        content=read(INIT_PY_FILE).format(**conf),
    )

    # create static dir
    static_dir = package_root / "static"
    static_dir.mkdir(exist_ok=True)

    # example scripts: scripts.py
    SCRIPTS_PY = "scripts.py"
    write(dst_fp=package_root / SCRIPTS_PY, content=read(SCRIPTS_PY).format(**conf))

    # example.py for example scripts
    EXAMPLE_PY = "example.py"
    write(dst_fp=package_root / EXAMPLE_PY, content=read(EXAMPLE_PY).format(**conf))

    # [LOGGING]
    summary = "\n".join(
        [
            f"[bold]Python project '{project}' is ready.[/bold]",
            " - Build Package: 'python -m build', python package 'build' is required.",
            " - Upload to PyPI: 'twine upload dist/*', python package 'twine is required.",
        ]
    )
    print()
    console.print(Panel(summary))
