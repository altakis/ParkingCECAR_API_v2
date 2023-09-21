# Parking CECAR
## API de reconocimiento v2
Debido a que el proceso de reconocimiento de placas requiere una cantidad variable de tiempo y no se puede asegurar que no
se pierdan peticiones en algun tipo de "limite de tiempo de peticion" se ha decidido separar el procesamiento de la peticion
inicial e implementar un message broker que coordine como proceso en segundo plano el procesameinto de imagenes.

## Instalacion
Estos pasos estan descritos para el sistema operativo de windows:

1. Copia el projecto a traves del comando de git clone:
```bash
git clone https://github.com/ReadingShades/ParkingCECAR_API_v2.git
```
3. Crea un entorno virtual: 
```bash
python -m venv venv
```
4. Activa el entorno virtual:
```bash
venv/Scripts/Activate.bat
```
6. Instala las librerias requisito a traves de pip:
```bash
pip install -r requirements.txt
```
7. Ejecuta la aplicacion a traves del comando:
```bash
python -m manage runserver
```

## MIT
### The MIT License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
