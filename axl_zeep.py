#! /usr/bin/python3
# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * axl_zeep.py
# *
# * Cisco AXL Python
# *
# * Copyright (C) 2021 Carlos Sanz <carlos.sanzpenas@gmail.com>
# *
# *  This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License
# * as published by the Free Software Foundation; either version 2
# * of the License, or (at your option) any later version.
# *
# *  This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# *------------------------------------------------------------------
# *
# Import Modules

from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth

from CiscoAXL import *

#from zeep import Client, Settings, Plugin, xsd
from zeep import Client, Settings, Plugin
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
#from zeep.exceptions import Fault
from prettytable import PrettyTable
from configobj import ConfigObj

import getopt
import logging

import sys
import platform
import time
import uuid
import os
import csv
import urllib3
#import json
import pprint

class PrettyLog():
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return pprint.pformat(self.obj)

# Argumentos pasados por linea de comandos
def parse_command_line(args):
    logger.debug('Ha entrado en la funcion parse_command_line()')
    # Creamos las variables globales que vamos a tener que utilizar en el resto del Script
    global csv_config_file
    global element_config_file
    global cspconfigfile
    try:
        # Aceptamos 
        opts, args = getopt.getopt(args[1:],"hc:f:",["help", "config-file=", "csv-file="])
    except getopt.GetoptError as err:
        print (str(err))
        logger.info(get_usage())
        sys.exit(2)

    """
     * options:
     *       -c, --config-file <Config file>
    """
    for option, args in opts:
        if option in ("-h", "--help"):
            logger.debug('Mostrando la Ayuda')
            logger.info(get_usage())
            sys.exit()
        elif option in ("-c", "--config-file"):
            logger.debug('Se ha pasado un fichero de configuracion')
            element_config_file = 'conf/' + args
            logger.info('Ha seleccionado el fichero de configuracion: %s' % (element_config_file))
            cspconfigfile = ConfigObj(element_config_file)
        elif option in ("-f", "--csv-file"):
            logger.debug('Se ha pasado un fichero de carga masiva')
            csv_config_file = 'csv/' + args
            logger.info('Ha seleccionado el fichero de carga masiva: %s' % (csv_config_file))

    # No se ha pasado un fichero de configuracion como argumento del script
    if(element_config_file==None):
        logger.info(get_usage())
        csp_table_file=PrettyTable(['id', 'Filename'])
        csp_table_id=0
        csp_dir = 'conf/'
        csp_file = []
        logger.debug('Buscamos todos los archivos *.cfg del directorio conf/')
        for file in os.listdir(csp_dir):
            if file.endswith(".cfg"):
                csp_file.append(file)
                csp_table_file.add_row([csp_table_id,file])
                csp_table_id += 1
        logger.debug('El numero de ficheros de configuracion es: %d',csp_table_id)
        # Si solo tenemos un fichero de configuracion, vamos a utilizar ese fichero, en caso contrario se pedira que nos digan que fichero de configuracion tenemos que utilizar.
        if csp_table_id == 1:
            element_config_file = csp_dir + csp_file[0]
            logger.info('Ha seleccionado el fichero de configuracion: %s' % (element_config_file))
            cspconfigfile = ConfigObj(element_config_file)
            return {'Status':True,'Detail': element_config_file}
        else:
            print (csp_table_file)
            csp_file_config = input('Seleccione el archivo de configuracion: ')
            if int(csp_file_config) > csp_table_id - 1:
                logger.error('Ha seleccionado un fichero erroneo')
                return False
            else:
                element_config_file = csp_dir + csp_file[int(csp_file_config)]
                logger.info('Ha seleccionado el fichero de configuracion: %s' % (element_config_file))
                cspconfigfile = ConfigObj(element_config_file)
                return {'Status':True,'Detail': element_config_file}
    return True

# Help function
def get_usage():
    logger.debug('Ha entrado en la funcion get_usage()')
    return "Uso: -c <Config file> -f <CSV File>"

# This class lets you view the incoming and outgoing http headers and/or XML
class MyLoggingPlugin(Plugin):
    def ingress(self, envelope, http_headers, operation):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers
    
    def egress(self, envelope, http_headers, operation, binding_options):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers

# Funcion para crear el cliente SOAP que atacara a Cisco Unified Communications Manager
def client_soap(config_file):
    logger.debug('Ha entrado en la funcion client_soap()')
    csp_cmserver = cspconfigfile['CUCM']['server']
    csp_username = cspconfigfile['CUCM']['user']
    csp_password = cspconfigfile['CUCM']['pass']
    csp_version  = cspconfigfile['CUCM']['version']

    if platform.system() == 'Windows':
        logger.debug('El sistema operativo es: %s' % (platform.system()))
        wsdl = 'file:////' + os.getcwd().replace ("\\","//") + '//Schema//CUCM//' + csp_version + '//AXLAPI.wsdl'
    else:
        logger.debug('El sistema operativo es: %s' % (platform.system()))
        wsdl = 'file://' + os.getcwd() + '/Schema/CUCM/' + csp_version + '/AXLAPI.wsdl'

    csp_location = 'https://' + csp_cmserver + '/axl/'

    logger.debug('El valor de csp_cmserver es: %s' % (csp_cmserver))
    logger.debug('El valor de csp_username es: %s' % (csp_username))
    logger.debug('El valor de csp_version es: %s' % (csp_version))
    logger.debug('El valor de csp_location es: %s' % (csp_location))
    logger.debug('El valor de wsdl es: %s' % (wsdl))

    # history shows http_headers
    global history
    history = HistoryPlugin()

    # The first step is to create a SOAP client session
    session = Session()

    # We avoid certificate verification by default, but you can uncomment and set
    # your certificate here, and comment out the False setting

    #session.verify = CERT
    session.verify = False
    session.auth = HTTPBasicAuth(csp_username, csp_password)

    transport = Transport(session=session, timeout=5, cache=SqliteCache())
    
    # strict=False is not always necessary, but it allows zeep to parse imperfect XML
    settings = Settings(strict=False, xml_huge_tree=True)

    try:
        csp_soap_client = Client(wsdl,
                                settings=settings,
                                transport=transport,
                                plugins=[MyLoggingPlugin(),history],
                                )
        service = csp_soap_client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding", csp_location)

    except:
        logger.error('Se ha producido un error al crear el cliente soap')
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha creado el cliente SOAP.')
        return service

# Funcion para dar de alta una sede
def AltaSede(logger, service, cspconfigfile, csv_config_file):
    '''
    # *------------------------------------------------------------------
    # * function AltaSede(logger, service, cspconfigfile, csv_config_file):
    # *
    # * Copyright (C) 2021 Carlos Sanz <carlos.sanzpenas@gmail.com>
    # *
    # *------------------------------------------------------------------
    '''
    logger.debug('Ha entrado en la funcion AltaSede')

    try:
        csv_file = open(csv_config_file, 'r', encoding='utf-8')
    except:
        logger.error('Se ha producido un error al abrir el archivo %s' % (csv_config_file))
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha abierto el archivo %s' % (csv_config_file))

        field_names = (
            'SiteID', 'UserFirstName', 'UserSurname', 'UserId', 'DirectoryNumber', 'routePartitionName' , 'ToIPModel', 'MACAddress', 'DID', 'CallingSearchSpace', 'VoiceMail', 'Locale', 'SD_Number', 'SD_Label' )
        file_reader = csv.DictReader(csv_file, field_names)

        #add_status = PrettyTable(['SiteID', 'UserFirstName', 'UserSurname', 'UserId', 'DirectoryNumber', 'routePartitionName' , 'ToIPModel', 'MACAddress', 'DID', 'CallingSearchSpace', 'VoiceMail', 'Locale', 'SD_Number', 'SD_Label'])
        for row in file_reader:
            # Borramos los espacios al principio y final que puedan tener
            row['SiteID']               = row['SiteID'].strip()
            row['UserFirstName']        = row['UserFirstName'].strip()
            row['UserSurname']          = row['UserSurname'].strip()
            row['DirectoryNumber']      = row['DirectoryNumber'].strip()
            row['ToIPModel']            = row['ToIPModel'].strip()
            row['MACAddress']           = row['MACAddress'].strip()
            row['DID']                  = row['DID'].strip()
            row['CallingSearchSpace']   = row['CallingSearchSpace'].strip()
            row['CSSForward']           = row['CallingSearchSpace'].strip()
            row['VoiceMail']            = row['VoiceMail'].strip()
            row['Locale']               = row['Locale'].strip()
            row['routePartitionName']   = row['routePartitionName'].strip()
            row['SD_Number']            = row['SD_Number'].strip()
            row['SD_Label']             = row['SD_Label'].strip()
            # Si no incluimos una Partition ponemos una por defecto
            if row['routePartitionName'] == '':
                row['routePartitionName'] = 'P_Internas'

            row['callPickupGroupName']  = 'CPG_OF' + row['SiteID'].strip()
            row['callManagerGroupName'] = 'CMG_Sub21CD1Sub06CD2'
            row['dateTimeSettingName'] = 'GT_Spain'
            
            if row['VoiceMail'] == 'YES':
                row['voiceMailProfileName'] = 'CAIXABANK_VMENABLED'
            else:
                row['voiceMailProfileName'] = 'NoVoiceMail'
            
            '''
            # Region
            cspaxl_Region.Add(logger, service, row)

            # Location
            cspaxl_Location.Add(logger, service, row)

            # Device Pool
            cspaxl_DevicePool.Add(logger, service, row)

            # Call Pick Up Group
            cspaxl_CallPickupGroup.Add(logger, service, row)

            # Line Group
            cspaxl_LineGroup.Add(logger, service, row)

            # Hunt List
            cspaxl_HuntList.Add(logger, service, row)

            # Hunt Pilot
            cspaxl_HuntPilot.Add(logger, service, row)

            # Line
            # Comprobamos si tenemos un Directory Number
            if row['DirectoryNumber'] == '':
                logger.error('No tenemos Directory Number y no podemos continuar en el actual registro')
                continue
            # Comprobamos el numero de Directory Numbers que han puesto - El separador es |
            if len(row['DirectoryNumber'].split('|')) == 1:
                logger.info('Tenemos que dar de alta un Directory Number')
                cspaxl_Line.Add(logger, service, row)
            else:
                logger.info('Tenemos que dar de alta varios Directory Number:: %s' % (row['DirectoryNumber'].split('|')))
                row_temp = row.copy()
                DN = row['DirectoryNumber'].split('|')
                Partiton = row['routePartitionName'].split('|')
                for x in range(0,len(DN)):
                    logger.info('Vamos a dar de alta el siguiente Directory Number: %s' % (DN[x]))
                    row_temp['DirectoryNumber']    = DN[x]
                    row_temp['routePartitionName'] = Partiton[x]
                    cspaxl_Line.Add(logger, service, row_temp)
            
            # Device
            cspaxl_Phone.Add(logger, service, row)

            # Translation Pattern
            cspaxl_TransPattern.Add(logger, service, row)
            '''
            # Add Line Group
            cspaxl_LineGroup.Add(logger, service, row)

# Main Function
if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-18s | %(filename)-18s:%(lineno)-4s | %(levelname)-9s | %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='Log/' + time.strftime("%Y%m%d-%H%M%S-") + str(uuid.uuid4()) + '.log',
                        filemode='w',
                        )
    urllib3.disable_warnings()
    element_config_file = None
    history = None
    logger = logging.getLogger('cisco.cucm.axl.zeep')
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)-18s | %(filename)-18s:%(lineno)-4s | %(levelname)-9s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console.setFormatter(formatter)
    console.setLevel=logger.setLevel
    logging.getLogger('').addHandler(console)

    logger.info('Estamos usando Python v%s' % (platform.python_version()))

    # Llamamos a la funcion parse_command_line
    if not parse_command_line(sys.argv):
        logger.error("Error in parsing arguments")
        sys.exit(1)

    logger.info('Se ha seleccionado el cliente: %s' % (cspconfigfile['INFO']['customer'].upper()))
    # Creamos nuestro cliente SOAP con los parametros del fichero de configuracion
    service = client_soap(element_config_file)

    AltaSede(logger, service, cspconfigfile, csv_config_file)

    logger.info('Se cerrara el programa')
    sys.exit()