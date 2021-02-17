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

Los archivos se tienen que guardar en el directorio `conf/`

## Fichero de carga
El archivo tiene que tener el siguiente formato:

```
Site ID,User First Name,User Surname,User Id (userPrincipalName),Directory Number,ToIP Model,MAC Address,DID,Calling Search Space,Voice Mail,Locale,SD_Number,SD_Label
```

Un ejemplo de fichero de alta sería:

```
0011,Carlos,Sanz Peñas,,6001102|6001181,P_Internas|P_LG_Oficinas,8811,SEPF0082F1B738C,913236708,CSS_All,NO,English United States,6001002|6001081,OF0010 - 02|OF0010 - 81
```

Es necesario que el archivo lo tengamos en el directorio `csv/`

## Ejecución

Para ejecutar el sctript tenemos:

```
python axl_zeep.py -c <Fichero_Configuracion> -f <Fichero_CSV>
```

### Logs
Por cada ejecución del script, se generara un fichero en el directorio `Log/`, donde podremos ver todo lo que ha estado haciendo el script.

```
2021-02-17 03:30:34 | axl_zeep.py       :324  | INFO      | Estamos usando Python v3.7.3
2021-02-17 03:30:34 | axl_zeep.py       :88   | INFO      | Ha seleccionado el fichero de configuracion: conf/NTT-Staging.cfg
2021-02-17 03:30:34 | axl_zeep.py       :93   | INFO      | Ha seleccionado el fichero de carga masiva: csv/0011.csv
2021-02-17 03:30:34 | axl_zeep.py       :331  | INFO      | Se ha seleccionado el cliente: NTT STAGING
2021-02-17 03:30:36 | axl_zeep.py       :199  | INFO      | Se ha creado el cliente SOAP.
2021-02-17 03:30:36 | axl_zeep.py       :222  | INFO      | Se ha abierto el archivo csv/0011.csv
2021-02-17 03:30:36 | cspaxl_Region.py  :81   | INFO      | Result:
+----------------------------------------+--------+
|                  UUID                  | Region |
+----------------------------------------+--------+
| {927B0A9C-3F59-8620-AF3D-25051E777ECE} | R_0011 |
+----------------------------------------+--------+
2021-02-17 03:30:37 | cspaxl_Location.py:81   | INFO      | Result:
+----------------------------------------+----------+
|                  UUID                  | Location |
+----------------------------------------+----------+
| {3161C539-757A-7F99-8834-9388DFE50C8E} |  L_0011  |
+----------------------------------------+----------+
2021-02-17 03:30:37 | cspaxl_DevicePool.py:85   | INFO      | Result:
+----------------------------------------+----------------+
|                  UUID                  |  Device Pool   |
+----------------------------------------+----------------+
| {2A97591F-0C57-3B8E-46B9-24ACD34C5A31} | DP_0011_ORANGE |
+----------------------------------------+----------------+
2021-02-17 03:30:37 | cspaxl_CallPickupGroup.py:68   | INFO      | Tenemos mas de una Partition en el registro
2021-02-17 03:30:37 | cspaxl_CallPickupGroup.py:87   | INFO      | Result:
+----------------------------------------+-------------------+
|                  UUID                  | Call Pickup Group |
+----------------------------------------+-------------------+
| {3BB9576C-0F8E-C427-E795-52C765C6CC7F} |     CPG_OF0011    |
+----------------------------------------+-------------------+
2021-02-17 03:30:37 | cspaxl_LineGroup.py:82   | INFO      | Result:
+----------------------------------------+------------+
|                  UUID                  | Line Group |
+----------------------------------------+------------+
| {C1EB4FC7-B9E0-8553-3E10-A870F36688F9} | LG_OF0011  |
+----------------------------------------+------------+
2021-02-17 03:30:38 | cspaxl_HuntList.py:87   | INFO      | Result:
+----------------------------------------+-----------+
|                  UUID                  | Hunt List |
+----------------------------------------+-----------+
| {643ADB01-7E41-BCA3-353A-9A6BA2BF57B1} | HL_OF0011 |
+----------------------------------------+-----------+
2021-02-17 03:30:38 | cspaxl_HuntPilot.py:105  | INFO      | Tenemos mas de una Partition en el registro
2021-02-17 03:30:38 | cspaxl_HuntPilot.py:131  | INFO      | Result:
+----------------------------------------+------------+
|                  UUID                  | Hunt Pilot |
+----------------------------------------+------------+
| {8D179901-A27B-46CE-799C-DE0E29CD032B} |  8001100   |
+----------------------------------------+------------+
2021-02-17 03:30:38 | axl_zeep.py       :288  | INFO      | Tenemos que dar de alta varios Directory Number:: ['6001102', '6001181']
2021-02-17 03:30:38 | axl_zeep.py       :293  | INFO      | Vamos a dar de alta el siguiente Directory Number: 6001102
2021-02-17 03:30:38 | cspaxl_Line.py    :134  | INFO      | Result:
+----------------------------------------+------------------+--------------------+
|                  UUID                  | Directory Number | routePartitionName |
+----------------------------------------+------------------+--------------------+
| {B508ABFC-2B4D-76CE-A8C6-8C0A2465AED3} |     6001102      |     P_Internas     |
+----------------------------------------+------------------+--------------------+
2021-02-17 03:30:38 | axl_zeep.py       :293  | INFO      | Vamos a dar de alta el siguiente Directory Number: 6001181
2021-02-17 03:30:39 | cspaxl_Line.py    :134  | INFO      | Result:
+----------------------------------------+------------------+--------------------+
|                  UUID                  | Directory Number | routePartitionName |
+----------------------------------------+------------------+--------------------+
| {D942BE08-92C9-87B0-E3EC-934F30BD42FF} |     6001181      |   P_LG_Oficinas    |
+----------------------------------------+------------------+--------------------+
2021-02-17 03:30:39 | cspaxl_Phone.py   :172  | INFO      | Tenemos que configurar Speed Dials
2021-02-17 03:30:39 | cspaxl_Phone.py   :198  | INFO      | El telefono SEPF0082F1B738C no existe en el CUCM
2021-02-17 03:30:39 | cspaxl_Phone.py   :214  | INFO      | Result:
+----------------------------------------+-----------------+-------------------+
|                  UUID                  |   Device Name   |    description    |
+----------------------------------------+-----------------+-------------------+
| {6A2DE04C-9A0C-7731-9135-B976D5F866D3} | SEPF0082F1B738C | Carlos Sanz Penas |
+----------------------------------------+-----------------+-------------------+
2021-02-17 03:30:39 | cspaxl_TransPattern.py:69   | INFO      | Tenemos mas de un Directory Number en el registro
2021-02-17 03:30:39 | cspaxl_TransPattern.py:80   | INFO      | Tenemos mas de una Partition en el registro
2021-02-17 03:30:40 | cspaxl_TransPattern.py:101  | INFO      | El Translation Pattern 913236708 en la Partition P_Internas no existe en el CUCM
2021-02-17 03:30:40 | cspaxl_TransPattern.py:117  | INFO      | Result:
+----------------------------------------+-----------+--------------------+
|                  UUID                  |  pattern  | routePartitionName |
+----------------------------------------+-----------+--------------------+
| {A53A7712-94AD-9AE1-B001-A290AC95C4CC} | 913236708 |     P_Internas     |
+----------------------------------------+-----------+--------------------+
2021-02-17 03:30:40 | cspaxl_Region.py  :74   | ERROR     | Could not insert new row - duplicate value in a UNIQUE INDEX column (Unique Index:).
2021-02-17 03:30:41 | cspaxl_Location.py:75   | ERROR     | Could not insert new row - duplicate value in a UNIQUE INDEX column (Unique Index:).
2021-02-17 03:30:41 | cspaxl_DevicePool.py:79   | ERROR     | Could not insert new row - duplicate value in a UNIQUE INDEX column (Unique Index:).
2021-02-17 03:30:41 | cspaxl_CallPickupGroup.py:65   | INFO      | Tenemos una sola Partition en el registro
2021-02-17 03:30:41 | cspaxl_CallPickupGroup.py:81   | ERROR     | Cannot insert or update pattern. A Call Pick Up Group exists with the same pattern and partition.
2021-02-17 03:30:41 | cspaxl_LineGroup.py:76   | ERROR     | Could not insert new row - duplicate value in a UNIQUE INDEX column (Unique Index:).
2021-02-17 03:30:41 | cspaxl_HuntList.py:81   | ERROR     | Could not insert new row - duplicate value in a UNIQUE INDEX column (Unique Index:).
2021-02-17 03:30:41 | cspaxl_HuntPilot.py:102  | INFO      | Tenemos una sola Partition en el registro
2021-02-17 03:30:41 | cspaxl_HuntPilot.py:125  | ERROR     | Cannot insert or update pattern. A Hunt Pilot exists with the same pattern and partition.
2021-02-17 03:30:41 | axl_zeep.py       :285  | INFO      | Tenemos que dar de alta un Directory Number
2021-02-17 03:30:42 | cspaxl_Line.py    :134  | INFO      | Result:
+----------------------------------------+------------------+--------------------+
|                  UUID                  | Directory Number | routePartitionName |
+----------------------------------------+------------------+--------------------+
| {2FC868F4-3D3F-94CD-3E3F-7521CE523CDA} |     6001101      |     P_Internas     |
+----------------------------------------+------------------+--------------------+
2021-02-17 03:30:42 | cspaxl_Phone.py   :170  | INFO      | No tenemos que configurar Speed Dials
2021-02-17 03:30:42 | cspaxl_Phone.py   :198  | INFO      | El telefono SEPFF082F1B738C no existe en el CUCM
2021-02-17 03:30:42 | cspaxl_Phone.py   :214  | INFO      | Result:
+----------------------------------------+-----------------+-------------------+
|                  UUID                  |   Device Name   |    description    |
+----------------------------------------+-----------------+-------------------+
| {39E6C0E7-953B-9D23-86FE-AE379B56DDB5} | SEPFF082F1B738C | Carlos Penas Sanz |
+----------------------------------------+-----------------+-------------------+
2021-02-17 03:30:42 | cspaxl_TransPattern.py:66   | INFO      | Tenemos una solo Directory Number en el registro
2021-02-17 03:30:42 | cspaxl_TransPattern.py:77   | INFO      | Tenemos una sola Partition en el registro
2021-02-17 03:30:42 | cspaxl_TransPattern.py:101  | INFO      | El Translation Pattern 913236706 en la Partition P_Internas no existe en el CUCM
2021-02-17 03:30:42 | cspaxl_TransPattern.py:117  | INFO      | Result:
+----------------------------------------+-----------+--------------------+
|                  UUID                  |  pattern  | routePartitionName |
+----------------------------------------+-----------+--------------------+
| {8E158A1D-94E0-A957-FF62-B54A0684AA35} | 913236706 |     P_Internas     |
+----------------------------------------+-----------+--------------------+
2021-02-17 03:30:42 | axl_zeep.py       :337  | INFO      | Se cerrara el programa
```