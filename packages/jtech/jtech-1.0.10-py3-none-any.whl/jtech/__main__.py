import argparse
import socket

import requests
import subprocess
from pkg_resources import parse_version
import colorama
import pkg_resources
import textwrap3
import platform

from jtech.project.create_project import CreateProject


def check_internet_connection():
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=3)
        return True
    except OSError:
        return False


def read_banner():
    banner_path = pkg_resources.resource_filename('jtech', 'resources/banner/banner.txt')
    with open(banner_path, 'r') as file:
        banner = file.read()
    return banner


def check_update(current_version):
    package_name = "jtech"
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    data = response.json()
    latest_version = data["info"]["version"]

    if parse_version(latest_version) > parse_version(current_version):
        print(f"Uma nova versão ({latest_version}) está disponível. Deseja atualizar? (y/n)")
        choice = input()

        if choice.lower() == "y":
            subprocess.run(["pip", "install", "--upgrade", package_name])
            print("Atualização realizada com sucesso!")
    else:
        print("Você já está usando a versão mais recente.")


def get_linux_distribution():
    with open('/etc/os-release', 'r') as f:
        lines = f.readlines()

    dist_info = {}
    for line in lines:
        key, value = line.strip().split('=')
        dist_info[key] = value.strip('"')

    return dist_info.get('NAME'), dist_info.get('VERSION')


def print_info_system(version_cli):
    system = platform.system()
    release = platform.release()
    machine = platform.machine()

    linux_distribution, linux_version = get_linux_distribution()

    print("System Information:")
    print("-------------------")
    print(f"System:         {system}")
    print(f"Distribution:   {linux_distribution}")
    print(f"Version:        {linux_version}")
    print(f"Release:        {release}")
    print(f"Machine:        {machine}")
    print(f"CLI:            {version_cli}")


def main():
    if not check_internet_connection():
        print("===================================================================================")
        print("Sem conexão com a internet! Para continuar é necessário uma conexão com a internet.")
        print("===================================================================================")
        exit(-1)

    colorama.init()

    banner = read_banner()
    banner = banner.replace('${Ansi.GREEN}', colorama.Fore.GREEN)
    banner = banner.replace('${Ansi.RED}', colorama.Fore.RED)
    banner = banner.replace('${Ansi.DEFAULT}', colorama.Style.RESET_ALL)

    version = pkg_resources.require("jtech")[0].version
    banner = banner.replace("{}", version)
    print(textwrap3.fill(banner))

    parser = argparse.ArgumentParser()

    parser.add_argument('--version', action='store_true', help='Show version')

    parser.add_argument("--create", action='store_true', help='Create a Spring Boot Project')

    parser.add_argument("--gui", action='store_true', help='Open GUI Interface (for Dummies)')

    parser.add_argument("project_name", nargs='?',
                        help='Name of the project to be created. Ex: jtech --create sansys-sample')

    vargs = parser.parse_args()

    if vargs.create:
        check_update(version)
        project = CreateProject()
        if vargs.project_name:
            project.create(vargs.project_name)
        else:
            project.create()

    elif vargs.version:
        print_info_system(version)
        check_update(version)

    elif vargs.gui:
        check_update(version)
        from jtech.gui.main_window import open_gui_interface
        open_gui_interface()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
