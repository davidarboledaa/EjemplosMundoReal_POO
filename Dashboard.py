import os
import subprocess
import logging
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Configurar logging
logging.basicConfig(filename='dashboard.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def mostrar_codigo(ruta_script):
    """Muestra el contenido de un script."""
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            codigo = archivo.read()
            print(f"\n{Fore.CYAN}--- Código de {ruta_script} ---{Style.RESET_ALL}\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print(f"{Fore.RED}El archivo no se encontró.{Style.RESET_ALL}")
        logging.error(f"Archivo no encontrado: {ruta_script}")
        return None
    except Exception as e:
        print(f"{Fore.RED}Ocurrió un error al leer el archivo: {e}{Style.RESET_ALL}")
        logging.error(f"Error al leer el archivo {ruta_script}: {e}")
        return None

def ejecutar_codigo(ruta_script):
    """Ejecuta un script en una nueva terminal."""
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Unix-based systems
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(f"{Fore.RED}Ocurrió un error al ejecutar el código: {e}{Style.RESET_ALL}")
        logging.error(f"Error al ejecutar el script {ruta_script}: {e}")

def mostrar_menu():
    """Muestra el menú principal del dashboard."""
    ruta_base = os.path.dirname(__file__)

    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2'
    }

    while True:
        print(f"\n{Fore.GREEN}Menu Principal - Dashboard{Style.RESET_ALL}")
        for key in unidades:
            print(f"{key} - {unidades[key]}")
        print("0 - Salir")

        eleccion_unidad = input("Elige una unidad o '0' para salir: ")
        if eleccion_unidad == '0':
            print("Saliendo del programa.")
            break
        elif eleccion_unidad in unidades:
            mostrar_sub_menu(os.path.join(ruta_base, unidades[eleccion_unidad]))
        else:
            print(f"{Fore.RED}Opción no válida. Por favor, intenta de nuevo.{Style.RESET_ALL}")

def mostrar_sub_menu(ruta_unidad):
    """Muestra el submenú para seleccionar una subcarpeta."""
    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        print(f"\n{Fore.YELLOW}Submenú - Selecciona una subcarpeta{Style.RESET_ALL}")
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar al menú principal")

        eleccion_carpeta = input("Elige una subcarpeta o '0' para regresar: ")
        if eleccion_carpeta == '0':
            break
        else:
            try:
                eleccion_carpeta = int(eleccion_carpeta) - 1
                if 0 <= eleccion_carpeta < len(sub_carpetas):
                    mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[eleccion_carpeta]))
                else:
                    print(f"{Fore.RED}Opción no válida. Por favor, intenta de nuevo.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Opción no válida. Por favor, intenta de nuevo.{Style.RESET_ALL}")

def mostrar_scripts(ruta_sub_carpeta):
    """Muestra los scripts disponibles en una subcarpeta."""
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]

    while True:
        print(f"\n{Fore.BLUE}Scripts - Selecciona un script para ver y ejecutar{Style.RESET_ALL}")
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Regresar al submenú anterior")
        print("9 - Regresar al menú principal")

        eleccion_script = input("Elige un script, '0' para regresar o '9' para ir al menú principal: ")
        if eleccion_script == '0':
            break
        elif eleccion_script == '9':
            return  # Regresar al menú principal
        else:
            try:
                eleccion_script = int(eleccion_script) - 1
                if 0 <= eleccion_script < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[eleccion_script])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("No se ejecutó el script.")
                        else:
                            print(f"{Fore.RED}Opción no válida. Regresando al menú de scripts.{Style.RESET_ALL}")
                        input("\nPresiona Enter para volver al menú de scripts.")
                else:
                    print(f"{Fore.RED}Opción no válida. Por favor, intenta de nuevo.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Opción no válida. Por favor, intenta de nuevo.{Style.RESET_ALL}")

# Ejecutar el dashboard
if __name__ == "__main__":
    mostrar_menu()
    Explicación de los Cambios:
Colorama: agregue la biblioteca colorama para mejorar la presentación visual del menú.

Logging: implemente un sistema de registro para guardar errores en un archivo dashboard.log.

Mensajes de Error: mejore los mensajes de error para que sean más descriptivos y estén coloreados.

Comentarios: agregue comentarios descriptivos para cada función.
