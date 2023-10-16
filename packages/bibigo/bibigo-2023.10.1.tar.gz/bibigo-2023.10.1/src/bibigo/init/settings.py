from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from ..utils import read, write

console = Console(width=88)


################################################################
# init package
################################################################
def init_settings(root, verbose=False):
    # get project name from input
    fp = Path(root)
    project = fp.absolute().name

    # [WRITE FILES]
    overwritten = list()
    for FILE in [".gitignore", ".dockerignore", ".vscode/settings.json"]:
        _fp = fp / FILE
        confirm = True
        if _fp.exists():
            answer = input(f"'{_fp}' is exists. overwrite? (y/N) ")
            if answer.strip().lower() != "y":
                confirm = False
            else:
                overwritten += [FILE]
        if confirm:
            write(dst_fp=fp / FILE, content=read(FILE))

    # [LOGGING]
    if verbose:
        summary = [f"[bold]Settings for Project '{project}' is Ready.[/bold]"]
        if overwritten:
            summary += [" - [NOTE] " + ", ".join(overwritten) + " are overwritten."]
        console.print(Panel("\n".join(summary)))
