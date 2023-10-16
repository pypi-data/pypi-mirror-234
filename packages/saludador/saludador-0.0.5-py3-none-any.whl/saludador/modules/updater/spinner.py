# -*- coding: utf-8 -*-
"""
    updater.spinner
    ~~~~~~~~~~~~~~~

    Modulo que usa Progress.spinner para esperar algun proceso usando threads.

    :copyright: (c) 2023 by Jaime Andrés Feldman.
    :license: GPL3, see LICENSE for more details.
"""

import threading
import cursor
import time
import sys

def hide_cursor():
    sys.stdout.write("\033[?16;0t")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?16;1t")
    sys.stdout.flush()

# Función que muestra un spinner mientras espera
def show_spinner():

    cursor.hide()
    spin_symbols = "|/-\\"
    i = 0
    while not done_event.is_set():
        sys.stdout.write("\rChecking for updates... " + spin_symbols[i])
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(spin_symbols)
    sys.stdout.write('\b')
    sys.stdout.flush()
    print("         ")
    cursor.show()

# Evento para indicar cuando el hilo debe terminar
done_event = threading.Event()
spinner_thread = threading.Thread(target=show_spinner)

# Crear un hilo para mostrar el spinner
def start():
    spinner_thread.start()


# Detener el hilo del spinner
def stop():
    done_event.set()
    spinner_thread.join()


