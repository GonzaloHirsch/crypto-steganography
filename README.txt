# Trabajo Práctico de Criptografía y Seguridad (GRUPO 5)

El objetivo de este trabajo era poder realizar una implementación de Secreto Compartido en base al paper "Sistema de Imagen Secreta Compartida con Optimización de la Carga Útil" de Angelina Espejel-Trujillo, Iván Castillo-Camacho, Mariko Nakano-Miyatake, Héctor Pérez-Meana.


## Requerimientos

Se necesita Python 3 para poder ejecutar este programa. Idealmente cualquier versión superior a la 3.8.7 debería ser más que suficiente, pero versiones anteriores deberían también funcionar.

También se necesita la herramienta 'pip' (o 'pip3' en su defecto).

Para poder tener un mejor control del entorno utilizado en Pampero recomendamos utilizar 'virtualenv' (herramienta que ya viene en Pampero), para evitar problemas de dependencias. 


## Instalación

Antes de ejecutar el programa, es necesario instalar las dependencias. Para esto se usa 'pip' (o 'pip3' en su defecto).

Se ejecuta, estando en el root del directorio del proyecto, lo siguiente ('$>' es para indicar la terminal, no incluir en el comando ejecutado):

$> virtualenv env

Una vez creado el entorno (da un mensaje largo que se puede ignorar), ejecutar:

$> source env/bin/activate

Para poder activar el entorno virtual de Python 3. Se puede verificar que la versión en Pampero es 3.9.2 con:

$> python --version

Una vez configurado el entorno virtual, ejecutar el siguiente comando para instalar las dependencias:

$> pip install -r src/requirements.txt


## Ejecutar

Para poder ejecutar desde el root del directorio del proyecto se hace (manteniendo la sintaxis de la cátedra):

$> python src/main.py [d|r] <PATH_A_SECRETO> [4|5|6] <PATH_AL_DIRECTORIO>

Ejemplos del comando pueden ser:

Si se tiene un directorio 'imagenes' dentro de la carpeta del proyecto, y una imagen secreta llamada 'secret.bmp' también dentro del directorio:

$> python src/main.py d secret.bmp 4 imagenes/


## Creditos

Gonzalo Hirsch --> ghirsch@itba.edu.ar
Florencia Petrikovich --> fpetrikovich@itba.edu.ar
Rodrigo Manuel Navarro Lajous --> rnavarro@itba.edu.ar