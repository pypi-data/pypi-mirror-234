from pathlib import Path
from typing import List, Optional

from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from git import Repo, Tag
from git.objects import Commit
from poetry.core.constraints.version import Version
from poetry.poetry import Poetry

from poetry_git_version_plugin import config
from poetry_git_version_plugin.exceptions import (
    InvalidCanonPepVersionException,
    InvalidPepVersionException,
    InvalidVersionException,
    PluginException,
)
from poetry_git_version_plugin.utils import validate_version
from poetry_git_version_plugin.version_details import VersionDetail


class GitService(object):
    repo: Repo

    def __init__(self) -> None:
        path = Path.cwd()
        self.repo = Repo(path, search_parent_directories=True)

    @property
    def commits(self) -> List[Commit]:
        return list(self.repo.iter_commits())

    @property
    def current_commit(self) -> Commit:
        return self.repo.head.commit

    @property
    def tags(self) -> List[Tag]:
        return list(self.repo.tags)[::-1]

    def get_current_tag(self) -> Optional[Tag]:
        """Получение тега нынешнего коммита"""

        tags = list(self.repo.tags)[::-1]

        for tag in tags:
            if tag.commit == self.repo.head.commit:
                return tag

        return None

    def get_last_tag(self) -> Optional[Tag]:
        """Получение последнего тега нынешней ветки"""

        commits = set(self.commits)
        tags = self.tags

        for tag in tags:
            if tag.commit in commits:
                return tag

        return None

    def get_current_short_rev(self) -> str:
        return self.current_commit.name_rev[:7]

    def get_distance(self, from_commit: Commit, to_commit: Commit) -> int:
        return len(list(self.repo.iter_commits(f'{from_commit}..{to_commit}')))


class VersionService(object):
    io: IO
    plugin_config: config.PluginConfig

    git_service: GitService

    def __init__(self, io: IO, plugin_config: config.PluginConfig) -> None:
        self.io = io
        self.plugin_config = plugin_config

        self.git_service = GitService()

        self.version_maker = VersionDetail()

    def get_main_version(self) -> Optional[str]:
        tag = self.git_service.get_current_tag()

        if tag is None:
            return None

        self.version_maker.parse_tag(tag.name)
        self.version_maker.commit_hash = self.git_service.get_current_short_rev()

        return self.version_maker.format(self.plugin_config.version_format)

    def get_alpha_version(self):
        tag = self.git_service.get_last_tag()

        if tag is None:
            distance_from_commit = self.git_service.commits[-1]

        else:
            distance_from_commit = tag.commit
            self.version_maker.parse_tag(tag.name)

        self.version_maker.distance = self.git_service.get_distance(
            distance_from_commit,
            self.git_service.current_commit,
        )
        self.version_maker.commit_hash = self.git_service.get_current_short_rev()

        return self.version_maker.format(self.plugin_config.alpha_version_format)

    def __get_version(self) -> str:
        self.io.write(f'<b>{config.PLUGIN_NAME}</b>: Find git <b>current tag</b>... ', verbosity=Verbosity.VERBOSE)

        version = self.get_main_version()

        if version is not None:
            self.io.write_line(f'success, setting dynamic version to: {version}', Verbosity.VERBOSE)
            return version

        self.io.write_line('fail', Verbosity.VERBOSE)

        if not self.plugin_config.make_alpha_version:
            raise PluginException('No Git version found, not extracting dynamic version')

        self.io.write(f'<b>{config.PLUGIN_NAME}</b>: Make <b>alpha version</b>... ', verbosity=Verbosity.VERBOSE)

        version = self.get_alpha_version()

        self.io.write_line(f'success, setting dynamic version to: {version}', Verbosity.VERBOSE)

        return version

    def validate_version(self, version: str):
        try:
            validate_version(version)

        except InvalidPepVersionException as ex:
            self.io.write_line(ex.args[0], Verbosity.VERBOSE)

            if not self.plugin_config.ignore_pep440:
                raise ex

        except InvalidCanonPepVersionException as ex:
            self.io.write_line(ex.args[0], Verbosity.VERBOSE)

            if not self.plugin_config.ignore_public_pep440:
                raise ex

        except InvalidVersionException as ex:
            self.io.write_line(ex.args[0], Verbosity.VERBOSE)

            if not self.plugin_config.ignore_semver:
                raise ex

    def get_version(self) -> str:
        version = self.__get_version()
        self.validate_version(version)
        return version

    @classmethod
    def safe_get_version(cls, io: IO, poetry: Poetry) -> Optional[Version]:
        plugin_config = config.PluginConfig(poetry.pyproject)

        try:
            version = cls(io, plugin_config).get_version()
            return Version.parse(version)

        except Exception as ex:
            if not isinstance(ex, PluginException):
                ex = PluginException(ex)

            if not plugin_config.ignore_errors:
                raise ex

            io.write_error_line(f'{ex}. Ignore Exception.')

            return None
