import subprocess
import sys
from pathlib import Path
from venv import create


def build_project(*args):
    if not args:
        args = ["-w"]

    command = [sys.executable, "-m", "build", *args]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)  # noqa: S603


def install_project():
    wheel = next(iter(Path.cwd().glob("dist/*.whl")))
    userbase = Path.cwd().joinpath("build")
    userbase.mkdir()
    command = f"{sys.executable} -m pip install {str(wheel)} -t build"
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True, shell=True)  # noqa: S603, S602


def install_project_venv() -> Path:
    install_directory = Path.cwd().joinpath("build")
    create(install_directory, with_pip=True)

    env_python = str(install_directory.joinpath("bin", "python"))

    # Upgrade pip
    subprocess.check_call([env_python, "-m", "pip", "install", "--upgrade", "pip"])

    # Install the package. We don't know the name (well, we could, but I'm lazy)
    wheel = next(iter(Path.cwd().glob("dist/*.whl")))
    subprocess.check_call([env_python, "-m", "pip", "install", wheel])

    return install_directory
