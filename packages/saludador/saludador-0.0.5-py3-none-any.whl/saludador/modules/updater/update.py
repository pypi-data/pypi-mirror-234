# -*- coding: utf-8 -*-
"""
    updater.update
    ~~~~~~~~~~~~~~~

    Modulo que chequea y actualiza la versión del paquete con PyPi.

    :copyright: (c) 2023 by Jaime Andrés Feldman.
    :license: GPL3, see LICENSE for more details.
"""
import subprocess, sys, requests, time, readchar
import saludador.modules.updater.spinner as spinner

from   rich.console import Console

console = Console()

# Chequea la versión actual con la de PyPi.
def check_internet_connection():
    try:
        # Intenta hacer una solicitud HTTP a nic.cl
        response = requests.get("http://www.nic.cl", timeout=5)
        # Si la solicitud es exitosa (código de estado 200), hay conexión a Internet
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        # Si se produce una excepción de conexión, no hay conexión a Internet
        return False


# Función para verificar la versión actual del paquete
def get_installed_version(package_name):
    try:
        result = subprocess.check_output([sys.executable, "-m", "pip", "show", package_name])
        for line in result.decode("utf-8").split("\n"):
            if line.startswith("Version:"):
                return line.split(":")[1].strip()
        return None
    except subprocess.CalledProcessError:
        return None

# Función para obtener la última versión desde la API de PyPI
def get_latest_version_from_pypi(package_name):
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        data = response.json()
        return data["info"]["version"]
    except requests.exceptions.RequestException:
        return None

# Función que compara las las versones y determina si es necesario un update.
def check_versions(package_name) -> (str, str):

    current_verson = get_installed_version(package_name)
    pypi_verson    = get_latest_version_from_pypi(package_name)
    return (current_verson, pypi_verson)

# Función principal para el chequeo de actualizaciones.
def check_updates(package_name=None):
    # Chequea si existe conexión a internet.
    # - se implementa el Ctrl+C para captura de señal de termino.
    # Chequea si existe un update.
    # Si Existe un update informa por pantalla y consulta al usuario si desea actualizar.
    # Si el usuario acepta, muestra una barra rich con el progreso de descarga he instalación.
    # Genera un chequeo de Hash. (descarga el hash de la pagina pypi y la compara despues de la instación) 
    # Muestra información de la reciente actualización.
    try:
        if check_internet_connection():

            spinner.start()
            versions = check_versions(package_name)
            spinner.stop()
            if not versions[0] == versions[1]:
                version_actual = versions[0]
                ultima_version = versions[1]
                console.print(f"[[cyan]notice[/]] A new release is available: [red]{version_actual}[/] -> [green]{ultima_version}[/]") 
                exit = False 
                while not exit: 
                    # answer = input("Do you want to update?[Y/n/i]:d")
                    console.print(r"Do you want to update? [[yellow]y[/]es/[yellow]n[/]o/[yellow]i[/]nfo]:", end="")
                    answer = readchar.readchar()

                    if answer == 'i' or answer == 'I':
                        print("\nmensaje con info")
                    elif answer == 'n'or answer == 'N':
                        print("\nno actualiza nada..")
                        exit = True
                    elif answer == 'y' or answer == "Y" or answer == "\n":
                        print("\nactualizando!")
                        exit = True


    except KeyboardInterrupt:
        spinner.stop()
        print("Forced termination!")
        sys.exit(1)

