# Introduccion
En este carpeta se van a guardar todos los archivos que vamos a subir para hacer las configuraciones masivas.

# Formato del archivo
El archivo tiene que tener el siguiente formato:

```
Site ID,User First Name,User Surname,User Id (userPrincipalName),Directory Number,ToIP Model,MAC Address,DID,Calling Search Space,Voice Mail,Locale,SD_Number,SD_Label,Phone Button Template
```

Los valores que tenga el fichero no pueden tener el caracter coma, porque es el utilizado para separa los campos.

Un ejemplo de fichero de alta sería:

```
0011,Carlos,Sanz Peñas,,6001102|6001181,P_Internas|P_LG_Oficinas,8811,SEPF0082F1B738C,913236708,CSS_All,NO,English United States,6001002|6001081,OF0010 - 02|OF0010 - 81,Standard 8811 SIP
```

Es necesario que el archivo lo tengamos en el directorio _csv/_

Para ejecutar el sctript tenemos:

```
python axl_zeep.py -c <Fichero_Configuracion> -f <Fichero_CSV>
```
