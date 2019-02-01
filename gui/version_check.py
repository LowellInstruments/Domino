from urllib.request import urlopen
from urllib.error import URLError
import re
from distutils.version import LooseVersion


class VersionChecker:
    def __init__(self):
        self.remote = 'https://lowellinstruments.com/download_files'
        self.pattern = 'Domino_Installer_([0-9]+\.[0-9]+\.[0-9]+)\.exe'

    def get_latest_version(self):
        try:
            remote = urlopen(self.remote)
            text = remote.read().decode('IBM437')
            matches = re.findall(self.pattern, text)
        except URLError:
            return None

        if not matches:
            return None

        latest = '0.0.0'
        for version in matches:
            if LooseVersion(version) > LooseVersion(latest):
                latest = version
        return latest

    def is_latest(self, version):
        latest = self.get_latest_version()
        if not latest:
            return True

        if LooseVersion(version) >= LooseVersion(latest):
            return True
        else:
            return False
