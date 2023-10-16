import os
from subprocess import run
from argparse import ArgumentParser
import re
from dataclasses import dataclass


FORMAT = re.compile(r"^v?(\d+)\.(\d+)\.(?:(\d+)|beta(\d+)|alpha(\d+))$")


def read_version_string(string):
    if match := FORMAT.match(string):
        return tuple((-1 if (x is None) else int(x)) for x in match.groups())


def write_version_string(major, minor, patch, beta, alpha):
    if alpha >= 0:
        final = f'alpha{alpha}'
    elif beta >= 0:
        final = f'beta{beta}'
    elif patch >= 0:
        final = str(patch)
    return f"{major}.{minor}.{final}"


def git(command):
    result = run(['git'] + command.split(),
                 capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(result.stderr)
    return result.stdout.strip()


LEVELS = ['major', 'minor', 'patch', 'beta', 'alpha']


@dataclass
class Handler:

    set_current: list
    level: str = ''
    debug: bool = False

    @property
    def current(self):
        if not hasattr(self, '_current'):
            if self.set_current:
                self._current = read_version_string(
                    self.set_current[0].strip())
            else:
                branch = git("branch --show-current")
                tags = git(f"tag --merged {branch}")
                self._current = (0, 0, 0, -1, -1)
                for tag in tags.split('\n'):
                    if version := read_version_string(tag):
                        if version > self._current:
                            self._current = version
        if not self._current:
            raise RuntimeError(f"Incorrect or missing current version")
        return self._current

    def update_version(self):
        major, minor, patch, beta, alpha = self.current
        if self.level == 'major':
            major += 1
            minor = 0
            patch = 0
            beta = alpha = -1
        elif self.level == 'minor':
            minor += 1
            patch = 0
            beta = alpha = -1
        elif self.level == 'patch':
            patch += 1
            beta = alpha = -1
        elif self.level == 'beta':
            if patch < 0:
                beta = 1 if (beta < 0) else beta + 1
                alpha = -1
            else:
                minor += 1
                beta = 1
                patch = alpha = -1
        elif self.level == 'alpha':
            if patch < 0 and beta < 0:
                alpha = alpha + 1
            else:
                minor += 1
                alpha = 1
                patch = beta = -1
            patch = beta = -1
        return major, minor, patch, beta, alpha

    def do(self):
        version = self.update_version() if self.level else self.current
        print(write_version_string(*version))


def main():
    parser = ArgumentParser()
    parser.add_argument('level', choices=LEVELS, nargs='?')
    parser.add_argument('--set-current', '-s', action='store', nargs=1)
    namespace = parser.parse_args()
    handler = Handler(**vars(namespace))
    handler.do()
