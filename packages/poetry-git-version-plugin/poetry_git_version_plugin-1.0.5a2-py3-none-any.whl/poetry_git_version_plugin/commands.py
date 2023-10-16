from poetry.console.commands.command import Command

from poetry_git_version_plugin.exceptions import plugin_exception_wrapper


class GitVersionCommand(Command):
    name = 'git-version'

    @plugin_exception_wrapper
    def handle(self) -> None:  # pragma: no cover
        self.io.write_line(str(self.poetry.package.version))


class SetGitVersionCommand(Command):
    name = 'set-git-version'

    @plugin_exception_wrapper
    def handle(self) -> None:  # pragma: no cover
        version = str(self.poetry.package.version)

        try:
            self.poetry.pyproject.data['tool']['poetry']['version'] = version

        except KeyError as ex:
            self.io.write_line(f'Error with parsing pyproject: {ex}')
            return

        self.io.write_line(f'The new version has been installed: {version}')

        self.poetry.pyproject.save()
