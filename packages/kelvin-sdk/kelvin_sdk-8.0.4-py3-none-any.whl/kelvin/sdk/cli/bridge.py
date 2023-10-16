"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""

from typing import Optional

import click

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.utils.click_utils import ClickExpandedPath, KSDKCommand, KSDKGroup
from kelvin.sdk.lib.utils.logger_utils import logger


@click.group(cls=KSDKGroup)
def bridge() -> None:
    """
    Manage and view bridges.

    """


@bridge.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all available bridges in the platform.

    """
    from kelvin.sdk.interface import bridge_list

    return bridge_list(should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.argument("bridge_name", nargs=1, type=click.STRING, required=False)
def show(bridge_name: str) -> bool:
    """
    Show the details of a bridge.

    e.g. kelvin bridge show "my-bridge"
    """
    from kelvin.sdk.interface import bridge_show

    if bridge_name is None:
        bridge_name = input("Enter the name of the bridge you want to show: ")

    return bridge_show(bridge_name=bridge_name, should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.option("--cluster-name", type=click.STRING, required=False, help=KSDKHelpMessages.bridge_cluster_name)
@click.option("--bridge-name", type=click.STRING, required=False, help=KSDKHelpMessages.bridge_name)
@click.option("--protocol", type=click.STRING, required=False, help=KSDKHelpMessages.bridge_protocol)
@click.option(
    "--bridge-title",
    type=click.STRING,
    required=False,
    help=KSDKHelpMessages.bridge_title,
)
@click.option(
    "--bridge-config",
    type=ClickExpandedPath(exists=True),
    required=False,
    help=KSDKHelpMessages.bridge_config,
)
def deploy(
    cluster_name: str,
    bridge_name: str,
    protocol: str,
    bridge_title: str,
    bridge_config: str,
) -> bool:
    """
    Deploy a registry application to the Kelvin Cloud (based on a local app.yaml).

    \b
    Usage: kelvin bridge deploy --bridge-name "test-bridge" --cluster-name "my-cluster" --protocol "opc-ua" --bridge-config "/path/to/app.yaml"

    """
    from kelvin.sdk.interface import bridge_deploy
    from kelvin.sdk.lib.models.bridge.ksdk_bridge_deployment import BridgeDeploymentRequest

    if cluster_name is None:
        cluster_name = input("Enter the name of the cluster you want to deploy to: ")
    if bridge_name is None:
        bridge_name = input("Enter the name of the bridge you want to deploy: ")
    if protocol is None:
        protocol = input("Enter the protocol of the bridge you want to deploy: ")
    if bridge_config is None:
        bridge_config = input("Enter the path to the bridge config you want to deploy: ")

    bridge_deployment_request = BridgeDeploymentRequest(
        node_name=cluster_name,
        bridge_name=bridge_name,
        bridge_title=bridge_title,
        bridge_config=bridge_config,
        protocol=protocol,
    )

    return bridge_deploy(bridge_deployment_request=bridge_deployment_request).success


@bridge.command(cls=KSDKCommand)
@click.option(
    "--bridge-config",
    type=ClickExpandedPath(exists=True),
    required=False,
    help=KSDKHelpMessages.bridge_config,
)
@click.option("--name", type=click.STRING, required=False, help=KSDKHelpMessages.bridge_name)
def undeploy(
    bridge_config: Optional[str],
    name: Optional[str],
) -> bool:
    """
    Undeploy a bridge application.
    Either provide the bridge name to undeploy or a configuration file to extract it from.

    """
    from kelvin.sdk.interface import bridge_undeploy

    if not (bridge_config or name):
        logger.error("Unable to undeploy bridge. Either provide a bridge name or bridge config.")
        return False

    return bridge_undeploy(bridge_config=bridge_config, bridge_name=name).success
