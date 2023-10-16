# noinspection PyUnresolvedReferences
from pyplugin_installer.installer_data import repositories, plugins


__all__ = ["plugin_status"]


def plugin_status(plugin_key: str) -> str:
    all_plugins = plugins.all()
    if plugin_key in all_plugins:
        return all_plugins[plugin_key]["status"]
    return "Not Found"


# utils.reloadPlugin()
