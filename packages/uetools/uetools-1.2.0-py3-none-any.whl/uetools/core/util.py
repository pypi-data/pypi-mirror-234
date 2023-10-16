import re
import os
from pathlib import Path
from functools import lru_cache

_re_deduce_project_plugin = re.compile(
    r"(.*)(\\|/)(?P<Project>([A-Za-z0-9]*))(\\|/)Plugins(\\|/)(?P<Plugin>([A-Za-z0-9]*))(.*)"
)


def find_file_like(path, pat):
    path = Path(path)

    while path:
        results = list(path.glob(pat))

        if results:
            return results[0], path

        if path == path.parent:
            break

        path = path.parent

    return None, path


@lru_cache(maxsize=None)
def deduce_project_plugin(path):
    path = str(path)

    result = _re_deduce_project_plugin.search(path)
    if result:
        data = result.groupdict()
        return data["Project"], data["Plugin"]

    # Iteratively go up the tree looking for the plugin
    plugin, remain = find_file_like(path, "*.uplugin")

    if plugin:
        plugin = str(plugin.parent.name)

    project = deduce_project(path)
    return project, plugin


@lru_cache(maxsize=None)
def deduce_project(path):
    result, remain = find_file_like(path, "*.uproject")
    if result:
        return str(result.parent.name)
    return None


@lru_cache(maxsize=None)
def deduce_module(path):
    path, remain = find_file_like(path, "*Build..cs")
    return str(os.path.dirname(path))


if __name__ == "__main__":
    print(deduce_project_plugin(os.getcwd()))
    print(deduce_project(os.getcwd()))
