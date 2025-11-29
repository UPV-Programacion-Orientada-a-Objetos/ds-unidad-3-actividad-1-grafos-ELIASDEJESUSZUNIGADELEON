"""
NeuroNet - Launcher sin consola
Ejecuta la GUI sin mostrar la ventana de terminal
"""
import os
import sys

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar y ejecutar GUI
from gui.main_window import main

if __name__ == "__main__":
    main()
