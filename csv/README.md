# Introduccion
En este carpeta se van a guardar todos los archivos que vamos a subir para hacer las configuraciones masivas.

# Formato del archivo
El archivo tiene que tener el siguiente formato:

```
Site ID,User First Name,User Surname,User Id (userPrincipalName),Directory Number,ToIP Model,MAC Address,DID,Calling Search Space,Voice Mail,Locale
```

Un ejemplo de fichero de alta sería:

```
0011,Carlos,Sanz,carlos.sanz,6001101,8811,AABBCCDDEEFF,913236708,CSS_All,NO,Spanish Spain
```

Es necesario que el archivo lo tengamos en el directorio _csv/_

Para ejecutar el sctript tenemos:

```
python axl_zeep.py -c <Fichero_Configuracion> -f <Fichero_CSV>
```
