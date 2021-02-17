# CiscoCollab
Cisco Unified Communications Manager - AXL

Script para provisionar la configuración del Cisco Unified Communications Manager (CUCM) con python3

## Tareas
 - [ ] Crear usuario con el Role de AXL

## Requisitos
Es necesario tener un usuario de aplicación (Aplication User) con el Role de Standard AXL API Access, para poder realizar configuraciones utilizando AXL.

Una vez que hemos creado nuestro usuario tendremos que crearnos un entorno virtual en Python donde podamos instalar todas las librerias que son necesarias:

```
virtualenv CiscoAXL
```

Activamos nuestro entorno virtual:

```
source ../venv/ciscoaxl/bin/activate
```

Clonamos nuestro repositorio:

```
git clone https://github.com/sanzcarlos/CiscoAXL
```

Instalamos los paquetes que necesitamos para poder ejecutar nuestro script

```
pip install -r requirements.txt
```

## Fichero Configuración
Tenemos que crearnos un fichero para cada uno los cluster que queramos utilizar con nuestro script, el formato del archivo tiene que ser:

```
# Credenciales del servicio de LDAP
[INFO]
customer = Template
[LDAP]
name = "Template"
server = 
user = 
password = 
search_base = 
[CUCM]
server = 
user = 
pass = 
version = 
[CUC]
server =
user = 
pass = 
version =  
[CUP]
server =
user = 
pass = 
version =  
[UCCX]
server =
user = 
pass = 
version =  
[GMAIL]
username = 
from = 
password = 
smtpserver = 
smtpport = 
[SQL]
server = 
database = 
user = 
password = 
```

Los archivos se tienen que guardar en el directorio conf/