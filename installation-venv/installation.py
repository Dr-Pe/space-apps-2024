import os
import subprocess
import sys
from pathlib import Path



def crear_entorno(ruta_entorno):
    print(f"Creando entorno virtual en '{ruta_entorno}'...")
    subprocess.check_call([sys.executable, "-m", "venv", ruta_entorno])
    print("Entorno virtual creado.")


def instalar_bibliotecas(ruta_entorno, bibliotecas):
    pip_path = Path(ruta_entorno) / 'Scripts' / 'pip.exe'
    
    for biblioteca in bibliotecas:
        print(f"Instalando '{biblioteca}'...")
        subprocess.check_call([pip_path, "install", biblioteca])
    print("Bibliotecas instaladas.")

if __name__ == "__main__":
    ruta_entorno = input("Ingrese path del venv sin el nombre del mismo (ejemplo Windows ..\\):")
    ruta_entorno = ruta_entorno+".venv"
    crear_entorno(ruta_entorno)
    bibliotecas = [
        'numpy',
        'pygame',
        'colour-science',
    ]
    instalar_bibliotecas(ruta_entorno, bibliotecas)