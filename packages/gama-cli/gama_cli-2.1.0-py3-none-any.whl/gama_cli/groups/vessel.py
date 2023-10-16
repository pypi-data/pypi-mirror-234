import os
from typing import List, Optional
import click

from gama_config.gama_vessel import (
    Variant,
    Network,
    Mode,
    read_vessel_config,
    get_vessel_config_path,
    LogLevel,
    write_vessel_config,
    GamaVesselConfig,
)
from gama_cli.helpers import (
    call,
    docker_compose_path,
    get_project_root,
    docker_bake,
    get_gama_version,
    maybe_ignore_build,
    maybe_ignore_prod,
)
from python_on_whales.docker_client import DockerClient
from python_on_whales.utils import ValidPath


DOCKER_VESSEL = docker_compose_path("vessel/docker-compose.yaml")
DOCKER_VESSEL_PROD = docker_compose_path("vessel/docker-compose.prod.yaml")
DOCKER_VESSEL_DEV = docker_compose_path("vessel/docker-compose.dev.yaml")
DOCKER_VESSEL_NETWORK_SHARED = docker_compose_path("vessel/docker-compose.network-shared.yaml")
DOCKER_VESSEL_NETWORK_VPN = docker_compose_path("vessel/docker-compose.network-vpn.yaml")
DOCKER_VESSEL_NETWORK_HOST = docker_compose_path("vessel/docker-compose.network-host.yaml")

SERVICES = [
    "gama_ui",
    "gama_chart_tiler",
    "gama_chart_api",
    "gama_vessel",
    "gama_greenstream",
    "gama_docs",
]


def _get_compose_files(
    network: Network = Network.SHARED,
    variant: Variant = Variant.WHISKEY_BRAVO,
    prod: bool = False,
) -> List[ValidPath]:
    compose_files: List[ValidPath] = [DOCKER_VESSEL]
    if not prod:
        compose_files.append(DOCKER_VESSEL_DEV)

    compose_files.append(
        docker_compose_path(f"vessel/docker-compose.variant.{variant.value}.yaml")
    )

    if network == Network.SHARED:
        compose_files.append(DOCKER_VESSEL_NETWORK_SHARED)
    if network == Network.VPN:
        compose_files.append(DOCKER_VESSEL_NETWORK_VPN)
    if network == Network.HOST:
        compose_files.append(DOCKER_VESSEL_NETWORK_HOST)
    if prod:
        compose_files.append(DOCKER_VESSEL_PROD)

    return compose_files


def log_config(config: GamaVesselConfig):
    click.echo(click.style("[+] GAMA Vessel Config:", fg="green"))
    for attr, value in config.__dict__.items():
        click.echo(
            click.style(f" ⠿ {attr}: ".ljust(35), fg="white") + click.style(str(value), fg="green")
        )


@click.group(help="Commands for the vessel")
def vessel():
    pass


@click.command(name="build")
@click.argument(
    "service",
    required=False,
    type=click.Choice(SERVICES),
)
@click.argument("args", nargs=-1)
def build(service: str, args: List[str]):  # type: ignore
    """Build the vessel"""
    config = read_vessel_config()

    docker = DockerClient(
        compose_files=_get_compose_files(
            variant=config.variant,
        ),
        compose_project_directory=get_project_root(),
    )

    os.environ["GAMA_VARIANT"] = config.variant.value
    os.environ["GAMA_NAMESPACE_VESSEL"] = config.namespace_vessel
    os.environ["GAMA_NAMESPACE_GROUNDSTATION"] = config.namespace_groundstation

    if service:
        docker.compose.build([service])
        return

    docker.compose.build(["gama_ui", "gama_chart_tiler", "gama_chart_api", "gama_vessel"])


@click.command(name="bake")
@click.option(
    "--variant",
    type=click.Choice(Variant),  # type: ignore
    required=True,
    help="The variant to bake",
)
@click.option(
    "--version",
    type=str,
    required=True,
    help="The version to bake. Default: latest",
)
@click.option(
    "--push",
    type=bool,
    default=False,
    is_flag=True,
    help="Should we push the images to the registry? Default: False",
)
@click.argument("services", nargs=-1)
def bake(variant: Variant, version: str, push: bool, services: List[str]):  # type: ignore
    """Bakes the vessel docker containers"""
    compose_files = _get_compose_files(variant=variant)
    docker_bake(
        version=version,
        services=services,
        push=push,
        compose_files=compose_files,
    )


@click.command(name="test-ui")
def test_ui():  # type: ignore
    """Runs test for the ui"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.run("gama_ui", ["yarn", "test"])


@click.command(name="test-ros")
def test_ros():  # type: ignore
    """Runs test for the ros nodes"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.run(
        "gama_vessel",
        ["/bin/bash", "-c", "source /home/ros/.profile && platform ros test"],
    )


@click.command(name="test-e2e")
def test_e2e():  # type: ignore
    """Runs UI e2e tests (assuming all the containers are up)"""
    call("cd ./projects/gama_ui && yarn test:e2e")


@click.command(name="test")
def test():  # type: ignore
    """Runs test for the all vessel code"""
    call("gama_cli vessel test-ui")
    call("gama_cli vessel test-ros")


@click.command(name="lint-ui")
@click.argument("args", nargs=-1)
def lint_ui(args: List[str]):  # type: ignore
    """Runs lints for the ui"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.run("gama_ui", ["yarn", "lint", *args])


@click.command(name="type-generate")
def type_generate():  # type: ignore
    """Generates typescript types for all ros messages"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    docker.compose.run("gama_vessel", ["npx", "ros-typescript-generator"])


@click.command(name="up")
@click.option(
    "--build",
    type=bool,
    default=False,
    is_flag=True,
    help="Should we rebuild the docker containers? Default: False",
)
@click.argument(
    "service",
    required=False,
    type=click.Choice(SERVICES),
)
@click.argument("args", nargs=-1)
def up(
    build: bool,
    service: str,
    args: List[str],
):
    """Starts the vessel"""
    dev_mode = os.environ["GAMA_CLI_DEV_MODE"] == "true"

    config = read_vessel_config()
    build = maybe_ignore_build(dev_mode, build)
    prod = maybe_ignore_prod(dev_mode, config.prod)
    log_config(config)

    docker = DockerClient(
        compose_files=_get_compose_files(
            network=config.network,
            variant=config.variant,
            prod=prod,
        ),
        compose_project_directory=get_project_root(),
    )

    os.environ["GAMA_VERSION"] = get_gama_version()
    os.environ["GAMA_VARIANT"] = config.variant.value
    os.environ["GAMA_NAMESPACE_VESSEL"] = config.namespace_vessel
    os.environ["GAMA_NAMESPACE_GROUNDSTATION"] = config.namespace_groundstation
    os.environ["ROS_DOMAIN_ID"] = str(config.ros_domain_id)

    services = (
        [service]
        if service
        else [
            "gama_ui",
            "gama_chart_tiler",
            "gama_chart_api",
            "gama_vessel",
            "gama_greenstream",
            "gama_docs",
        ]
    )

    docker.compose.up(
        services,
        detach=True,
        build=build,
    )

    if config.extensions.lookout:
        docker.compose.up(
            ["lookout"],
            detach=True,
            build=build,
        )


@click.command(name="down")
@click.argument("args", nargs=-1)
def down(args: List[str]):  # type: ignore
    """Stops the vessel"""
    docker = DockerClient(
        compose_files=_get_compose_files(),
        compose_project_directory=get_project_root(),
    )
    # set timeout to 20 secs (default 10) to allow for graceful shutdown of rosbag et al
    docker.compose.down(timeout=20)


@click.command(name="install")
@click.option(
    "--variant",
    type=click.Choice(Variant),  # type: ignore
    help="Which variant of GAMA to install?",
)
def install(variant: Variant):  # type: ignore
    """Install GAMA on a vessel"""
    config = read_vessel_config()
    variant = variant or config.variant
    docker = DockerClient(
        compose_files=_get_compose_files(variant=variant),
        compose_project_directory=get_project_root(),
    )
    try:
        docker.compose.pull(
            [
                "gama_ui",
                "gama_chart_tiler",
                "gama_chart_api",
                "gama_vessel",
                "gama_greenstream",
                "gama_docs",
            ]
        )
    except Exception:
        click.echo(
            click.style(
                "Failed to pull GAMA files. Have you ran `gama authenticate` ?",
                fg="yellow",
            )
        )


@click.command(name="configure")
@click.option(
    "--variant",
    type=click.Choice(Variant),  # type: ignore
    help="The Variant",
)
@click.option(
    "--mode",
    type=click.Choice(Mode),  # type: ignore
    help="The Mode",
)
@click.option(
    "--log-level",
    type=click.Choice(LogLevel),  # type: ignore
    help="The Log Level",
)
@click.option(
    "--network",
    type=click.Choice(Network),  # type: ignore
    help="The Network",
)
@click.option(
    "--prod",
    type=bool,
    help="Whether to run in production mode",
)
def configure(variant: Optional[Variant], mode: Optional[Mode], log_level: Optional[LogLevel], network: Optional[Network], prod: Optional[bool]):  # type: ignore
    """Configure GAMA Vessel"""
    # Prompt the user only if no arguments are passed
    prompt_user = all(v is None for v in [variant, mode, log_level, network, prod])
    if not prompt_user:
        config = GamaVesselConfig()
        if variant is not None:
            config.variant = variant
        if mode is not None:
            config.mode = mode
        if log_level is not None:
            config.log_level = log_level
        if network is not None:
            config.network = network
        if prod is not None:
            config.prod = prod
        write_vessel_config(config)
    else:
        # Check if the file exists
        if os.path.exists(get_vessel_config_path()):
            click.echo(
                click.style(
                    f"GAMA Vessel config already exists: {get_vessel_config_path()}",
                    fg="yellow",
                )
            )
            result = click.prompt(
                "Do you want to overwrite it?", default="y", type=click.Choice(["y", "n"])
            )
            if result == "n":
                return

        try:
            config_current = read_vessel_config()
        except Exception:
            config_current = GamaVesselConfig()

        config = GamaVesselConfig(
            ros_domain_id=click.prompt(
                "ROS Domain ID",
                default=config_current.ros_domain_id,
                type=int,
            ),
            namespace_vessel=click.prompt(
                "Namespace Vessel",
                default=config_current.namespace_vessel,
            ),
            namespace_groundstation=click.prompt(
                "Namespace Groundstation",
                default=config_current.namespace_groundstation,
            ),
            variant=click.prompt(
                "Variant",
                default=config_current.variant,
                type=click.Choice([item.value for item in Variant]),
            ),
            ubiquity_user=click.prompt("Ubiquity username", default=config_current.ubiquity_user),
            ubiquity_pass=click.prompt("Ubiquity password", default=config_current.ubiquity_pass),
            ubiquity_ip=click.prompt("Ubiquity ip", default=config_current.ubiquity_ip),
            mode=click.prompt(
                "Mode",
                default=config_current.mode,
                type=click.Choice([item.value for item in Mode]),
            ),
            prod=click.prompt("Prod", default=config_current.prod, type=bool),
            network=click.prompt(
                "Network",
                default=config_current.network,
                type=click.Choice([item.value for item in Network]),
            ),
            log_level=click.prompt(
                "Log level",
                default=config_current.log_level,
                type=click.Choice([item.value for item in LogLevel]),
            ),
        )
        write_vessel_config(config)


@click.command(name="config")
def config():  # type: ignore
    """Read Config"""
    config = read_vessel_config()
    log_config(config)
