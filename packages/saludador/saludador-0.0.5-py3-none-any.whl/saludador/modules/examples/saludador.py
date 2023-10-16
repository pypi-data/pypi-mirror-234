# -*- coding: utf-8 -*-
"""
    examples.saludador
    ~~~~~~~~~~~~~~~~~~

    Modulo de pruebas, solo para probar el __init__ y la importación en el archivo main.

    :copyright: (c) 2023 by jaime feldman.
    :license: MIT, see LICENSE for more details.
"""

def saluda(name=None):
    if name is None:
        return "Hola, mundo python!"
    else:
        return f"Hola, {name}!"

