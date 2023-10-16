import sys
# from saludador.modules.examples import saluda
import saludador.modules.examples as saludador
import saludador.modules.updater  as updater


from rich import print
from saludador.launcher.__version__ import __VERSION__


def main():
    print(f"[[bold green]Hola mundo python[/]] version {__VERSION__}")
    print("probando el modulo salduador: ", saludador.saluda())
    print("\n[[cyan]test updater module[/]]")
    #print("\[[yellow]Comprobando conexion a internet[/]]:", end='')
    # if updater.check_internet_connection():
        # print("[green] Ok [/]")
    # else:
        # print("[red] Fail [/]")
    
    # Obteniendo la verisón actual del paquete.
    # current_version = updater.get_installed_version("saludador")
    # print(f"[[yellow]current version[/]]: {current_version}")

    # Obteniendo la última versón desde PyPi.
    # latest_version = updater.get_latest_version_from_pypi("saludador")
    # print(f"[[yellow]ultima versión disponible[/]]: {latest_version}")

    updater.check_updates("saludador")
    
if __name__ == "__main__":
    sys.exit(main())
