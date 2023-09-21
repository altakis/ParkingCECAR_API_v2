# Parking CECAR
## API de reconocimiento v1
Esta api se encarga de conectar el modelo de vision de computadoras con el resto del sistema a traves de un REST endpoint.

Se selecciono a Django REST framework como la base del proyecto pensando en el plan de expansion a futuro:
1. Seguridad
2. Testing
3. Performance testing

## Instalacion
Estos pasos estan descritos para el sistema operativo de windows:

1. Copia el projecto a traves del comando de git clone:
```bash
git clone https://github.com/ReadingShades/ParkingCECAR_API_v1.git
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

## Notas
De momento solo existen dos endpoints:
GET:
http://127.0.0.1:8000/detections/

Este retorno una lista completa de las detecciones existentes en la base de datos.

POST:
http://127.0.0.1:8000/detections/

Este crea una deteccion utilizando el siguiente formato como fuente:

```javascript
{
  "data": {
    "src_file": "string"
  },
  "options": {
    "pred_json_bin": boolean,
    "crop_json_bin": boolean
  }
}
```
data.src_file: string := Cadena de caracteres que contiene la posicion relativa o absoluta del archivo imagen fuente para realizar la deteccion

Por implementar:
options.pred_json_bin: bool = False := Comando opcional que solicita o no la representacion base64 de la imagen resultado de la prediccion
options.crop_json_bin: bool = False := Comando opcional que solicita o no la representacion base64 del recorte de la licencia 

Estas ultimas opciones no son recomendadas debido a que la transmision de objetos binarios a traves de JSON es posible, es lento y tiende a colgar la transmision. 
Sin embargo, se ofrece la opcion mientras se implementa un disco compartido o un CDN para servir estas imagenes

## MIT
### The MIT License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
