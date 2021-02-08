# CiscoCollab
Cisco Unified Communications Manager - AXL

Script para provisionar la configuración del Cisco Unified Communications Manager (CUCM) con python3

## Tareas
 - [ ] Crear usuario con el Role de AXL

## Requisitos
Es necesario tener un usuario de aplicación (Aplication User) con el Role de Standard AXL API Access, para poder realizar configuraciones utilizando AXL.

Una vez que hemos creado nuestro usuario tendremos que crearnos un entorno virtual en Python donde podamos instalar todas las librerias que son necesarias:

```
virtualenv CiscoCollab
```

Activamos nuestro entorno virtual:

```
source ../venv/ciscocollab/bin/activate
```

Clonamos nuestro repositorio:

```
git clone https://github.com/sanzcarlos/CiscoCollab.git
```

Instalamos los paquetes que necesitamos para poder ejecutar nuestro script

```
pip install -r requirements.txt
```