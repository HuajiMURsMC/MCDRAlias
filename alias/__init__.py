from typing import Dict
from copy import copy
import os

from mcdreforged.api.types import PluginServerInterface
from mcdreforged.api.utils.serializer import Serializable
from mcdreforged.api.command import Literal


class Config(Serializable):
    alias: Dict[str, str] = {}


def on_load(server: PluginServerInterface, old):
    config = server.load_config_simple(os.path.join("config", "alias.json"), in_data_folder=False, target_class=Config)
    cm = server._mcdr_server.command_manager
    for alia, original in config.alias.items():
        for plugin_root_node in cm.root_nodes.get(original, []):
            node = copy(plugin_root_node.node)
            node.literals = {alia}
            server.register_command(node)
