import subprocess

import requests

from cval_lib.utils.logger import Logger


class Library(str, Logger):
    def _network(self):
        self.warn('Failed to get information')

    def _not_installed(self):
        self.warn('The library is not installed')

    def _version(self):
        self.warn('Couldn\'t find the library version')

    @property
    def local_version(self) -> str:
        try:
            result = subprocess.check_output(["pip", "show", self]).decode("utf-8")
            lines = result.split("\n")
            for line in lines:
                if line.startswith("Version:"):
                    return line.split(":")[1].strip()
            self._version()
        except subprocess.CalledProcessError:
            self._not_installed()

    @property
    def latest_version(self):
        try:
            response = requests.get(f"https://pypi.org/pypi/{self}/json")
            data = response.json()
            latest_version = data["info"]["version"]
            return latest_version
        except requests.RequestException:
            self._network()


class LibraryChecker(Library):
    def __call__(self, *args, **kwargs):
        self.info(
            'Package versioning begins...'
        )
        self.info('To disable this option, set environ variable CVAL_CHECK_VERSION=False.')
        latest = self.latest_version
        local = self.local_version
        if latest != local and None not in (latest, local, ):
            self.warn(
                    f'Please update the package "{self}" to the version {latest} '
                    f'to avoid errors.'
                )
        else:
            self.info(f'Everything is fine! Installed cval-lib version is {local}.')
