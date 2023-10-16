# Poetry Git Version Plugin

Poetry plugin to set package version based on git tag.

[![PyPI](https://img.shields.io/pypi/v/poetry-git-version-plugin)](https://pypi.org/project/poetry-git-version-plugin/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-git-version-plugin)](https://pypi.org/project/poetry-git-version-plugin/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/poetry-git-version-plugin)](https://gitlab.com/rocshers/python/poetry-git-version-plugin)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/poetry-git-version-plugin/branch/release/graph/badge.svg?token=RPFNZ8SBQ6)](https://codecov.io/gitlab/rocshers:python/poetry-git-version-plugin)
[![Downloads](https://static.pepy.tech/badge/poetry-git-version-plugin)](https://pepy.tech/project/poetry-git-version-plugin)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/poetry-git-version-plugin)](https://gitlab.com/rocshers/python/poetry-git-version-plugin)

## Functionality

- **Git tag** parsing
- **Alpha version** making
- Setting found or generated version as package **poetry.version**
- Maintenance of **PEP 440**
- [Command](#poetry-git-version) to output a new version
- [Command](#poetry-set-git-version) to update the pyproject version

## Quick start

```bash
poetry self add poetry-git-version-plugin
poetry git-version # Write package version based on git tag
poetry build # Build package with version based on git tag
```

## Dependencies

Installed `Git` and:

```toml
[tool.poetry.dependencies]
python = ">=3.8"
poetry = ">=1.2.2"
```

## Configs

### MAKE ALPHA VERSION

If the tag is not found on the HEAD, then the version is built based on the last found tag and the HEAD.

- type: bool
- Default = true
- Result: 1.3.2a5

```toml
# Environment
export PACKAGE_VERSION_MAKE_ALPHA_VERSION=true
# pyproject.toml
[tool.poetry-git-version-plugin]
make_alpha_version = true
```

### MAIN VERSION FORMAT

Format for version.

Main version is used if there is git tag on HEAD.

- Type: str
- Default = `'{raw_version}'`
- Example:
  - version_format = '{version}+{commit_hash}' -> `1.3.2+5babef6`
  - version_format = '{major}-{minor}-{patch}' -> `1-3-2`

[Available variables](#versions-variables)

```toml
# Environment
export PACKAGE_VERSION_VERSION_FORMAT='{version}+{commit_hash}'
# pyproject.toml
[tool.poetry-git-version-plugin]
version_format = '{version}+{commit_hash}'
```

Notes:

- distance - is always 0

### ALPHA VERSION FORMAT

Format for alpha version.

Alpha version is used if there is no git tag on HEAD.

- Type: str
- Default = `'{version}a{distance}'`
- Example:
  - alpha_version_format = '{version}a{distance}' -> `1.3.2a5`
  - alpha_version_format = '{version}a{distance}+{commit_hash}' -> `1.3.2a5+5babef6`

[Available variables](#versions-variables)

```toml
# Environment
export PACKAGE_VERSION_ALPHA_VERSION_FORMAT='{version}a{distance}'
# pyproject.toml
[tool.poetry-git-version-plugin]
alpha_version_format = '{version}a{distance}'
```

### Ignore errors

Three variables to **ignore errors**

- Type: bool
- Default = true

```toml
# Ignore mismatch error PEP 440 version format
## Environment
export PACKAGE_VERSION_IGNORE_PEP440=true
## pyproject.toml
[tool.poetry-git-version-plugin]
ignore_pep440 = true

# Ignore mismatch error PEP 440 public version format
## Environment
export PACKAGE_VERSION_IGNORE_PUBLIC_PEP440=true
## pyproject.toml
[tool.poetry-git-version-plugin]
ignore_public_pep440 = true

# Ignore all errors
# including version not found errors
## Environment
export PACKAGE_VERSION_IGNORE_ERRORS=true
## pyproject.toml
[tool.poetry-git-version-plugin]
ignore_errors = true
```

## Version's variables

When creating a version, you can use a custom template and use prepared variables.

You can see the current list in the [sources](https://gitlab.com/rocshers/python/poetry-git-version-plugin/-/blob/release/poetry_git_version_plugin/version_details.py)

- `major`: The major version.
- `minor`: The minor version.
- `patch`: The patch version.
- `version`: Combines major, minor, and patch versions as a formatted string.
- `distance`: Indicates the distance from the last version.
- `commit_hash`: Stores the commit hash associated with the version.
- `raw_version`: The original git tag.
- `pre_release`: Contains information about pre-release version identifiers.
- `build_metadata`: Holds metadata related to the build or version.

## Commands

### poetry git-version


```bash
$ poetry git-version # Write package version based on git tag
1.3.2a5+5babef6
```

### poetry set-git-version


```bash
$ poetry git-version # Set new version in pyproject 
The new version has been installed: 1.3.2a5+5babef6

$ cat pyproject.toml | grep version
version = "1.3.2a5+5babef6"
```

## Use cases

### Publishing python package to pypi via poetry with version equal to git tag

.gitlab-ci.yml:

```yaml
pypi:
  stage: publishing
  image: python:3.10
  tags:
    - docker
  script:
    - poetry self add poetry-git-version-plugin
    - poetry config repositories.pypi https://upload.pypi.org/legacy/
    - poetry config pypi-token.pypi ${PYPI_TOKEN}
    - poetry publish -r pypi --build
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

- When creating a git tag: new package with version == {TAG}
- When pushing to CI_DEFAULT_BRANCH: new package with version == {TAG}a{N}

### Publishing python package to private pypi via poetry with version equal to git tag and commit hash

.gitlab-ci.yml:

```yaml
pypi:
  stage: publishing
  image: python:3.10
  tags:
    - docker
  script:
    - export PACKAGE_VERSION_ALPHA_VERSION_FORMAT='{version}a{distance}+{commit_hash}'
    - poetry self add poetry-git-version-plugin
    - poetry config repositories.gitlab "https://gitlab.com/api/v4/projects/$CI_PROJECT_ID/packages/pypi"
    - poetry config http-basic.gitlab gitlab-ci-token "$CI_JOB_TOKEN"
    - poetry publish -r gitlab --build
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

- When creating a git tag: new package with version == {TAG}
- When pushing to CI_DEFAULT_BRANCH: new package with version == {TAG}a{N}+{COMMIT_HASH}

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/poetry-git-version-plugin/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/poetry-git-version-plugin>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
