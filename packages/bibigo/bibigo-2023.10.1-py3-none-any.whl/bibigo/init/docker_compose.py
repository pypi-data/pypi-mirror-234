import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from ..exceptions import CancelInit
from ..utils import read, write

console = Console(width=88)


################################################################
# init package
################################################################
def init_stack(root):
    from InquirerPy import prompt

    # get service name from input
    fp = Path(root)
    service = fp.absolute().name

    # get private pypi url
    domain = os.getenv("DOMAIN") or "example.com"

    # set setup configuration
    deploy_conf = [
        {"type": "input", "name": "service", "default": service, "message": "Service Name"},
        {"type": "input", "name": "image", "default": "hello-world:latest", "message": "Image"},
        {"type": "input", "name": "command", "default": "/hello", "message": "Container Command"},
        {
            "type": "input",
            "name": "mode",
            "default": "replicated",
            "message": "Deploy Mode ('replicated' or 'global')",
        },
        {"type": "input", "name": "role", "default": "worker", "message": "Deploy Placement ('manager' or 'worker')"},
        {"type": "input", "name": "replicas", "default": "1", "message": "Replicas (No. of Containers)"},
        {"type": "input", "name": "http-entrypoint", "default": "web", "message": "Traefik Entrypoint for HTTP"},
        {
            "type": "input",
            "name": "https-entrypoint",
            "default": "websecure",
            "message": "Traefik Entrypoint for HTTPS",
        },
        {
            "type": "input",
            "name": "http-redirect",
            "default": "http-redirect",
            "message": "Traefik Middlware for HTTP Redirect",
        },
        {"type": "input", "name": "certresolver", "default": "lego", "message": "Certificate Resolver"},
        {"type": "input", "name": "traefik-network", "default": "traefik", "message": "Docker Network for Traefik"},
        {"type": "input", "name": "domain", "default": f"{service}.{domain}", "message": "Domain for Your Service"},
        {"type": "input", "name": "port", "default": "3000", "message": "Service Port"},
        {"type": "confirm", "name": "confirm", "message": "Confirm"},
    ]

    # user input
    conf = prompt(deploy_conf)
    confirm = conf.pop("confirm")
    if not confirm:
        raise CancelInit

    # [WRITE FILES]
    DOCKER_COMPOSE_FILE = "docker-compose.yml"
    write(dst_fp=fp / DOCKER_COMPOSE_FILE, content=read(DOCKER_COMPOSE_FILE).format(**conf))

    # [LOGGING]
    summary = "\n".join(
        [
            f"[bold]docker-compose.yml for '{service}' is ready.[/bold]",
        ]
    )
    print()
    console.print(Panel(summary))
