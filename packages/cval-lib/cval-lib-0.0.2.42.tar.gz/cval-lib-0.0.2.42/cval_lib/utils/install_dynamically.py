import subprocess
import sys
import warnings


def install_libs(*libs: str) -> None:
    for lib in libs:
        command = ["pipenv", "install", lib]
        try:
            subprocess.check_call(command)
        except Exception:
            warnings.warn('pipenv is not found. skipping')
            command = [sys.executable, "-m", "pip", "install", lib]
            subprocess.check_call(command)

