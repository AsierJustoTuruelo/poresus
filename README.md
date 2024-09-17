# Multi-Scanner Tool

Esta herramienta proporciona una serie de analizadores y escáneres que pueden extraer información de URLs específicas, incluyendo metadatos de archivos, vulnerabilidades de seguridad, direcciones de Bitcoin, favicons, entre otros.

## Instalación

Antes de ejecutar la herramienta, debes instalar las siguientes dependencias:

sudo apt install tor
pip install mmh3
pip install mutagen
pip install stem

## Uso
El programa acepta diferentes argumentos para ejecutar los escáneres disponibles. A continuación se describen los pasos básicos para ejecutar la herramienta y los escáneres que puedes utilizar.

Ejecución Básica
Para ejecutar la herramienta, usa el siguiente comando en la terminal:

python poresus.py -opcion <ruta_al_archivo_de_URLs>
Donde ruta_al_archivo_de_URLs es un archivo de texto que contiene una lista de URLs (una por línea) que quieres analizar.

### Escáneres Disponibles
La herramienta admite múltiples escáneres. Puedes especificar uno o más escáneres utilizando los siguientes argumentos:

-b, --bitcoin: Ejecuta el extractor de direcciones de Bitcoin.

-bf, --bruteforce: Ejecuta el escáner de fuerza bruta.

-e, --etag: Ejecuta el escáner de ETag.

-f, --favicon: Descarga y analiza el favicon de los sitios.

-fi, --fileinput: Valida las entradas de archivos.

-fh, --filehashes: Escanea y verifica los hashes de archivos.

-bm, --binarymetadata: Escanea metadatos de archivos binarios.

-em, --excelmetadata: Escanea metadatos de archivos Excel.

-gm, --gifmetadata: Escanea metadatos de archivos GIF.

-pm, --pdfmetadata: Escanea metadatos de archivos PDF.

-pwm, --pptmetadata: Escanea metadatos de archivos PowerPoint.

-wm, --wordmetadata: Escanea metadatos de archivos Word.

-mm, --mediametadata: Escanea metadatos de archivos de medios.

-tm, --txtmetadata: Escanea metadatos de archivos de texto.

-im, --imagemetadata: Escanea metadatos de imágenes.

-gs, --googleids: Extrae identificadores de servicios de Google.

-gh, --gzipheader: Escanea cabeceras Gzip.

-hh, --hostname: Escanea los nombres de host.

-hi, --htmlinfo: Analiza información HTML.

-me, --mailextractor: Extrae direcciones de correo electrónico de HTML.

-os, --otherservices: Analiza otros servicios detectados.

-pn, --phonenumbers: Extrae números de teléfono.

-php, --phpserver: Escanea información del servidor PHP.

-si, --serverinfo: Escanea información del servidor.

-ss, --serverstatus: Verifica el estado del servidor.

-rs, --socialnets: Escanea redes sociales vinculadas.

-sqli, --sqlinjection: Escanea vulnerabilidades de inyección SQL.

-vi, --inputvalidator: Valida la entrada de usuarios.

-xss, --xss: Escanea vulnerabilidades XSS.

-db, --database: Escanea tipos de base de datos.

-all, --all: Ejecuta todos los escáneres disponibles.

#### Ejemplo de Uso
Para ejecutar el extractor de direcciones de Bitcoin:

python tu_script.py -b ruta_al_archivo_de_URLs.txt
Para ejecutar todos los escáneres en un conjunto de URLs:

python tu_script.py --all ruta_al_archivo_de_URLs.txt

#### Dependencias de Diccionarios
Si ejecutas el escáner de fuerza bruta (--bruteforce), necesitarás los archivos de diccionario de nombres de usuario y contraseñas. Asegurarse de tener estos archivos en el siguiente directorio:

usernames_file: ./dics/usernames.txt

passwords_file: ./dics/passwords.txt
