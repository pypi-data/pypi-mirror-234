from __future__ import annotations

from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry

from poetry_git_version_plugin import config
from poetry_git_version_plugin.commands import GitVersionCommand, SetGitVersionCommand
from poetry_git_version_plugin.exceptions import plugin_exception_wrapper
from poetry_git_version_plugin.services import VersionService


class PoetryGitVersionPlugin(Plugin):
    """Плагин определения версии по гит тегу"""

    @plugin_exception_wrapper
    def activate(self, poetry: Poetry, io: IO):  # pragma: no cover
        io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Init', Verbosity.VERBOSE)

        version = VersionService.safe_get_version(io, poetry)

        if version is not None:
            poetry.package.version = version

        io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Finished\n', Verbosity.VERBOSE)


class PoetryGitVersionApplicationPlugin(ApplicationPlugin):
    commands = [GitVersionCommand, SetGitVersionCommand]
