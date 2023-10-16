import sys
import os
import re
import json
import semver
import functools
from urllib.request import Request, urlopen, HTTPError

import ssl

from . import util

PROD_PYPI_INDEX = "https://pypi.org/pypi"
TEST_PYPI_INDEX = "https://test.pypi.org/pypi"
MOCKED = False
MOCK_VERSIONS = {
    "pypi": ["0.1.7", "1.4.3", "1.4.4", "1.4.5", "1.4.6-rc.1"],
    "test": ["0.1.7", "1.4.3", "1.4.4", "1.4.5"],
    "tags": ["0.1.2", "0.1.3", "1.4.4", "1.4.5"],
}

RELEASE_SCOPE_BETA = "beta"
RELEASE_SCOPE_RELEASE = "release"
RELEASE_SCOPE_CANDIDATE = "candidate"

RELEASE_TOKENS = {
    RELEASE_SCOPE_BETA: "beta",
    RELEASE_SCOPE_RELEASE: None,
    RELEASE_SCOPE_CANDIDATE: "rc",
}


VERSION_POLICY = {
    "patch": "A bug fix",
    "minor": "A new feature",
    "major": "A breaking change",
}


class Bumper(object):
    """A class to help the user bump the version."""

    def __init__(self, repo, pip_name):
        self.repo = repo
        self.pip_name = pip_name
        self.version_filename = os.path.join(self.repo.working_dir, "VERSION")
        self.current_version = _read_version_file(self.version_filename)
        self.versions = self.get_versions()

    def latest_test_version(self):
        """Return the latest version on test.pypi.org."""
        return self.latest_version("test")

    def latest_pypi_version(self):
        """Return the latest version on pypi.org."""
        return self.latest_version("pypi")

    def latest_tag_version(self):
        """Return the latest tag from github."""
        return self.latest_version("tags")

    def latest_version(self, *sources):
        """Return the latest version from a list of versions."""
        if not sources:
            sources = ["test", "pypi", "tags"]
        return sorted_versions(
            [v for source in sources for v in self.versions[source]]
        )[-1]

    def get_versions(self):
        """Fetch the latest tags and PyPi versions."""
        if MOCKED:
            return MOCK_VERSIONS
        else:
            return {
                "test": self.get_pypi_versions(index=TEST_PYPI_INDEX),
                "pypi": self.get_pypi_versions(),
                "tags": self.get_tags(),
            }

    def get_pypi_versions(self, index=PROD_PYPI_INDEX):
        """
        Return a list of all PyPi versions for the named package.
        """
        return _get_pypi_versions(self.pip_name, index=index)

    def get_tags(self):
        """Return a list of all tags in the repo."""
        return sorted_versions([str(tag) for tag in self.repo.tags])

    def version_options(self, release_scope=RELEASE_SCOPE_BETA):
        if release_scope == RELEASE_SCOPE_BETA:
            sources = ["test", "pypi", "tags"]
        else:
            sources = ["pypi", "tags"]
        token = RELEASE_TOKENS[release_scope]
        reference_version = self.latest_version(*sources)
        result = get_version_options(reference_version, token=token)
        for i in range(len(result)):
            result[i] = {
                "label": result[i],
                "value": result[i],
            }

        return result

    def versions_table(self, max_versions=10):
        """Return a table of versions where the columns are the sources, and the rows are the versions."""
        sources = ["test", "pypi", "tags"]
        source_labels = [
            util.blue("Internal PyPi"),
            util.green("Production PyPi"),
            util.magenta("Repository Tags"),
        ]
        table = {}
        for source in sources:
            for version in sorted_versions(self.versions[source])[-max_versions:]:
                if version not in table:
                    table[version] = {"tags": False, "pypi": False, "test": False}
                table[version][source] = True

        # now convert the table to a list of dicts sorted in reverse
        result_table = [source_labels]
        versions = sorted_versions(table.keys())
        versions.reverse()
        for version in versions:
            result_table.append(
                [
                    util.blue(version) if table[version]["test"] else "",
                    util.green(version) if table[version]["pypi"] else "",
                    util.magenta(version) if table[version]["tags"] else "",
                ]
            )
        return result_table

    def validate_generic_version(self, version):
        """Validate that the version is a valid semver string."""
        if not semver.Version.is_valid(version):
            return f"Version {version} is not a valid semver string."
        version = semver.Version.parse(version)
        if version in self.versions["pypi"]:
            return f"Version {version} has already been released to PyPi."
        if version in self.versions["tags"]:
            return f"Version {version} has already been tagged in the repo."
        if version in self.versions["test"]:
            return f"Version {version} has already been released to Test PyPi."
        return None

    def validate_beta_version(self, version):
        """Validate that the version is a valid beta version."""
        problem = self.validate_generic_version(version)
        if problem:
            return problem
        version = semver.Version.parse(version)
        regex = re.compile(r"beta\.\d+")
        if not (version.prerelease and regex.match(version.prerelease)):
            return f"Version {version} is not a beta version like '1.2.3-beta.4'."
        return None

    def validate_candidate_version(self, version):
        """Validate that the version is a valid release candidate version."""
        problem = self.validate_generic_version(version)
        if problem:
            return problem
        version = semver.Version.parse(version)
        regex = re.compile(r"rc\.\d+")
        if not (version.prerelease and regex.match(version.prerelease)):
            return f"Version {version} is not a release candidate version like '1.2.3-rc.4'."
        return None

    def validate_release_version(self, version):
        """Validate that the version is a valid release version."""
        problem = self.validate_generic_version(version)
        if problem:
            return problem
        version = semver.Version.parse(version)
        if version.prerelease is None and version.build is None:
            return None
        return f"Version {version} is not a valid full release version like '1.2.3'."


def pypi_to_semver(version):
    """Convert a PyPi version to a semver."""
    pypi_version_regex = re.compile(r"(\d+)\.(\d+)\.(\d+)((rc|a|b)(\d+))?")
    match = pypi_version_regex.match(version)
    if not match:
        return None
    major, minor, patch, prerelease, prerelease_type, prerelease_num = match.groups()
    if prerelease_type:
        prerelease_type = {"rc": "rc", "a": "alpha", "b": "beta"}[prerelease_type]
        prerelease = f"-{prerelease_type}.{prerelease_num}"
    return f"{major}.{minor}.{patch}{prerelease or ''}"


def semver_to_pypi(version):
    version = semver.Version.parse(version)
    prerelease = ""
    if version.prerelease:
        prerelease_type, prerelease_num = version.prerelease.split(".")
        prerelease_type = {"rc": "rc", "alpha": "a", "beta": "b"}[prerelease_type]
        prerelease = f"{prerelease_type}{prerelease_num}"
    return f"{version.major}.{version.minor}.{version.patch}{prerelease or ''}"


def sorted_versions(versions):
    """Sort a list of versions."""
    return sorted(versions, key=functools.cmp_to_key(semver.compare))


def _read_version_file(filename):
    """Pull the version from the VERSION file."""
    version = util.first_nonblank_line(filename)
    if not version:
        sys.stderr.write(
            f"Can't get version string from the version file: {filename}. using 0.0.1\n"
        )
        return "0.0.1"
    return version if semver.Version.is_valid(version) else "0.0.1"



def _get_pypi_versions(pip_name, index):
    url = f"{index}/{pip_name}/json"
    print(url)
    
    request = Request(url=url, headers={'User-Agent': 'Mozilla/5.0', "Accept": "application/json"} )
    
    # https://stackoverflow.com/q/69692910
    ssl._create_default_https_context = ssl._create_unverified_context


    try:
        response = urlopen(request)
    except HTTPError as err:
        print("ERROR:", err)
        return ["0.0.0"]
    code = response.code
    if code != 200:
        print("code:", code)
        return  ["0.0.0"]

    raw_data = response.read()
    response_encoding = response.headers.get_content_charset("utf-8")
    decoded_data = raw_data.decode(response_encoding)
    data = json.loads(decoded_data)
    if "releases" not in data:
        return ["0.0.0"]
    versions = data["releases"]
    versions = [pypi_to_semver(v.strip()) for v in versions]
    return sorted_versions([v for v in versions if semver.Version.is_valid(v)])


def get_version_options(latest_version, token=None):
    """Return a list of the most likely versions to bump to

    See the tests for examples.
    """
    latest = semver.Version.parse(latest_version)
    if not token:
        return _get_release_options(latest)
    latest_version_token = latest.prerelease and latest.prerelease.split(".", 1)[0]
    if latest_version_token and (latest_version_token != token):
        if latest_version_token < token:
            return _get_later_prerelease_options(latest, token)
        return _get_earlier_prerelease_options(latest, token)
    return _get_any_prerelease_options(latest, token)


def _get_release_options(latest):
    if latest.prerelease:
        latest = latest.replace(prerelease=None)
        return [
            str(latest),
            str(latest.next_version(part="minor")),
            str(latest.next_version(part="major")),
        ]
    return [
        str(latest.next_version(part="patch")),
        str(latest.next_version(part="minor")),
        str(latest.next_version(part="major")),
    ]


def _get_any_prerelease_options(latest, token):
    return [
        str(latest.next_version(part="prerelease", prerelease_token=token)),
        str(latest.bump_minor().bump_prerelease(token=token)),
        str(latest.bump_major().bump_prerelease(token=token)),
    ]


def _get_later_prerelease_options(latest, token):
    latest = latest.replace(prerelease=None)
    return [
        str(latest.bump_prerelease(token=token)),
        str(latest.bump_minor().bump_prerelease(token=token)),
        str(latest.bump_major().bump_prerelease(token=token)),
    ]


def _get_earlier_prerelease_options(latest, token):
    latest = latest.replace(prerelease=None)
    return [
        str(latest.next_version(part="prerelease", prerelease_token=token)),
        str(latest.bump_minor().bump_prerelease(token=token)),
        str(latest.bump_major().bump_prerelease(token=token)),
    ]
