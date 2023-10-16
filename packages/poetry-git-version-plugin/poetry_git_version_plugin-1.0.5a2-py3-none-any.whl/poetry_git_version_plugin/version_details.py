from poetry_git_version_plugin.regex_compiles import VERSION_UNIVERSAL_REGEX


class VersionDetail(object):
    major: int
    minor: int
    patch: int
    raw_version: str
    distance: int
    commit_hash: str

    # Compile of major.minor.patch
    version: str

    pre_release: str
    build_metadata: str

    def __init__(self) -> None:
        self.distance = 0
        self.commit_hash = '00000000'
        self.parse_tag('0.0.0')

    def parse_tag(self, raw_tag: str):
        self.raw_version = raw_tag

        reg = VERSION_UNIVERSAL_REGEX.search(raw_tag)
        reg_dict = {}

        if reg is not None:
            reg_dict = reg.groupdict()

        self.major = int(reg_dict.get('major', 0))
        self.minor = int(reg_dict.get('minor', 0))
        self.patch = int(reg_dict.get('patch', 0))
        self.version = f'{self.major}.{self.minor}.{self.patch}'

        self.pre_release = reg_dict.get('pre_release', '')
        self.build_metadata = reg_dict.get('build_metadata', '')

    def format(self, version_format: str):  # noqa:A003
        return version_format.format(**self.__dict__)
