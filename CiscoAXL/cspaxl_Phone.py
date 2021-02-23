# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_Phone.py
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
import sys
import os
import suds
import ssl
import re
from unicodedata import normalize
from unittest.case import _AssertRaisesContext
from prettytable import PrettyTable

def String2ASCI (logger,text):
    # *------------------------------------------------------------------
    # * function String2ASCI(csp_text)
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
    # Source: https://es.stackoverflow.com/questions/135707/c%C3%B3mo-puedo-reemplazar-las-letras-con-tildes-por-las-mismas-sin-tilde-pero-no-l

    text = re.sub(r"([^n\u0300-\u036f]|)[\u0300-\u036f]+", r"\1", normalize( "NFD", text), 0, re.I)
    text = normalize( 'NFC', text)
    logger.debug('Texto ASCII: %s' % (text))
    return (text)

def Add(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Add(logger,csp_soap_client,cucm_variable_axl)
    # *
    # * Copyright (C) 2016 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    # Mandatory (name, product, class, protocol, protocolSide, devicePoolName, commonPhoneConfigName, locationName, useTrustedRelayPoint, phoneTemplateName, primaryPhoneName, builInBridgeStatus, packeCaptureMode, certificateOperation, deviceMobilityMode)
    logger.debug('Se ha entrado en la funcion Add del archivo cspaxl_Phone.py')
    axl_cucm = {}
    axl_cucm['class'] = 'Phone'
    if cucm_variable_axl['ToIPModel'][0:3] == 'SIP':
        axl_cucm['product'] = 'Third-party SIP Device (Advanced)'
    elif cucm_variable_axl['ToIPModel'][0:6] == 'Jabber':
        axl_cucm['product'] = 'Cisco Unified Client Services Framework'
    else:
        axl_cucm['product'] = 'Cisco ' + cucm_variable_axl['ToIPModel']
    axl_cucm['protocolSide'] = 'User'
    if cucm_variable_axl['ToIPModel'][0:2] == '39' or \
        cucm_variable_axl['ToIPModel'][0:2] == '78' or \
        cucm_variable_axl['ToIPModel'][0:6] == 'ATA 19' or \
        cucm_variable_axl['ToIPModel'][0:2] == '88' or \
        cucm_variable_axl['ToIPModel'][0:2] == '99' or \
        cucm_variable_axl['ToIPModel'][0:3] == 'SIP':
        axl_cucm['protocol'] = 'SIP'
    else:
        axl_cucm['protocol'] = 'SCCP'

    logger.debug('El protocolo utilizado por el telefono es: %s ' % (axl_cucm['protocol']))

    if cucm_variable_axl['ToIPModel'][0:2] == '39' or \
        cucm_variable_axl['ToIPModel'][0:3] == 'ATA':
        csp_axl_max = '2'
        csp_axl_busy = '1'
    else:
        csp_axl_max = '4'
        csp_axl_busy = '2'
    if cucm_variable_axl['ToIPModel'][0:3] == 'SIP':
        axl_cucm['securityProfileName'] = 'Third-party SIP Device Advanced - Standard SIP Non-Secure Profile'
    else:
        axl_cucm['securityProfileName'] = 'Cisco ' + cucm_variable_axl['ToIPModel'] + ' - Standard ' + axl_cucm['protocol'] + ' Non-Secure Profile'
    axl_cucm['locationName']          = 'L_' + cucm_variable_axl['SiteID']
    axl_cucm['devicePoolName']        = 'DP_' + cucm_variable_axl['SiteID'] + '_ORANGE'
    axl_cucm['useTrustedRelayPoint']  = 'Default'
    axl_cucm['commonPhoneConfigName'] = 'Standard Common Phone Profile'
    axl_cucm['builtInBridgeStatus']   = 'Default'
    axl_cucm['packetCaptureMode']     = 'None'
    axl_cucm['certificateOperation']  = 'No Pending Operation'
    axl_cucm['deviceMobilityMode']    = 'Default'
    if cucm_variable_axl['UserId'] != '':
        axl_cucm['ownerUserName']     = cucm_variable_axl['UserId']
        axl_cucm['digestUser']        = cucm_variable_axl['UserId']
    axl_cucm['userLocale'] = cucm_variable_axl['Locale']
    if cucm_variable_axl['ToIPModel'][0:3] == 'ATA':
        axl_cucm['name'] = 'ATA' + cucm_variable_axl['MACAddress'][-12:]
    else:
        axl_cucm['name'] = 'SEP' + cucm_variable_axl['MACAddress'][-12:]
    axl_cucm['description'] = cucm_variable_axl['UserFirstName'] + ' ' + cucm_variable_axl['UserSurname']

    # Añadimos la linea
    axl_cucm_display = cucm_variable_axl['UserFirstName'] + ' ' + cucm_variable_axl['UserSurname']
    axl_cucm_display_ascii = String2ASCI(logger,axl_cucm_display)

    DN = cucm_variable_axl['DirectoryNumber'].split('|')
    Partiton = cucm_variable_axl['routePartitionName'].split('|')
    # Comprobamos cuantos Directory Number tenemos que asociar a un Device
    if len(DN) == 1:
            axl_cucm_line = {'index': 1,
                         'display': axl_cucm_display[0:30],
                         'displayAscii': axl_cucm_display_ascii[0:30],
                         'e164Mask': cucm_variable_axl['DID'],
                         'label': axl_cucm_display[0:30],
                         'recordingMediaSource': 'Gateway Preferred',
                         'dirn': {'pattern': cucm_variable_axl['DirectoryNumber'], 'routePartitionName': cucm_variable_axl['routePartitionName']},
                         #'associatedEndusers': {'enduser': {'userId': cucm_variable_axl['UserId']}},
                         'maxNumCalls': csp_axl_max,
                         'busyTrigger': csp_axl_busy}
    else:
        axl_cucm_line = [ ]
        for x in range(0,len(DN)):
            axl_cucm_line.append({'index': x + 1,
                         'display': axl_cucm_display[0:30],
                         'displayAscii': axl_cucm_display_ascii[0:30],
                         'e164Mask': cucm_variable_axl['DID'],
                         'label': axl_cucm_display[0:30],
                         'recordingMediaSource': 'Gateway Preferred',
                         'dirn': {'pattern': DN[x], 'routePartitionName': Partiton[x]},
                         #'associatedEndusers': {'enduser': {'userId': cucm_variable_axl['UserId']}},
                         'maxNumCalls': csp_axl_max,
                         'busyTrigger': csp_axl_busy})

    # Limitamos el numero de caracteres de las variables
    if cucm_variable_axl['SD_Number'] == '':
        logger.info('No tenemos que configurar Speed Dials')
    else:
        logger.info('Tenemos que configurar Speed Dials')
        axl_cucm_sd = [ ]
        SD_N = cucm_variable_axl['SD_Number'].split('|')
        SD_L = cucm_variable_axl['SD_Label'].split('|')
        for x in range(0,len(SD_N)):
            axl_cucm_sd.append({'index': x + 1,
                         'dirn': SD_N[x],            
                         'label': SD_L[x]})
        axl_cucm['speeddials']  = {'speeddial': axl_cucm_sd}

    axl_cucm['lines']       = {'line': axl_cucm_line}
    axl_cucm['name']        = axl_cucm['name'][:128]
    axl_cucm['description'] = axl_cucm['description'][:128]

    # Comprobamos que el telefono no existe
    try:
        csp_soap_returnedTags = {'name':'','description':'','devicePoolName':'','callingSearchSpaceName':''}
        csp_soap_searchCriteria = {'name': axl_cucm['name']}
        result = csp_soap_client.listPhone(csp_soap_searchCriteria,csp_soap_returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}

    else:
        if (result['return'] == None):
            logger.info('El telefono %s no existe en el CUCM' % (axl_cucm['name']))
        else:
            logger.info('El telefono %s existe en el CUCM' % (axl_cucm['name']))
            return {'Status': False, 'Detail': axl_cucm['name']}
    # Damos de alta el telefono
    try:
        result = csp_soap_client.addPhone(axl_cucm)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['UUID','Device Name','description'])
        csp_table.add_row([result['return'][:], axl_cucm['name'], String2ASCI(logger,axl_cucm['description'])])
        csp_table_response = csp_table.get_string(fields=['UUID', 'Device Name', 'description'],
                                                  sortby="UUID").encode('latin-1')
        logger.info('Result:\n%s' % (csp_table_response.decode("utf-8")))
        return {'Status': True,'Detail':csp_table_response}

def Get(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Get(logger,csp_soap_client,cucm_variable_axl)
    # *
    # * Copyright (C) 2018 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    # Mandatory (MACAddress)
    logger.debug('Se ha entrado en la funcion Get del archivo cspaxl_Phone.py')
    try:
        result = csp_soap_client.getPhone(name=cucm_variable_axl['MACAddress'])
    except:
        logger.debug(sys.exc_info())
        logger.error(str(sys.exc_info()[1],'uft-8'))
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        logger.info('Result:\n%s' % (result))
        return {'Status': True,'Detail':result}

def List(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function List(logger,csp_soap_client,cucm_variable_axl)
    # *
    # * Copyright (C) 2018 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    # Mandatory (pattern,usage,routePartitionName)

    try:
        csp_soap_returnedTags = {'name': '', 'description': '', 'ownerUserName': ''}
        csp_soap_searchCriteria = {'name': '%' + cucm_variable_axl + '%'}
        result = csp_soap_client.service.listPhone(csp_soap_searchCriteria,csp_soap_returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['id','name','description','ownerUserName'])
        for x in range(0, len(result['return']['phone'])):
            csp_table.add_row([x,result['return']['phone'][x]['name'],result['return']['phone'][x]['description'],result['return']['phone'][x]['ownerUserName']['value'] ])
        csp_table_response = csp_table.get_string(fields=['id','name','description','ownerUserName'], sortby="id").encode('latin-1')
        logger.info('\n\n' + str(csp_table_response,'latin-1')  + '\n')
        return {'Status':True,'Detail':csp_table_response}

'''
def Remove(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Remove(logger,csp_soap_client,cucm_variable_axl)
    # *
    # * Copyright (C) 2016 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    # Mandatory (pattern,usage,routePartitionName)
    try:
        result = csp_soap_client.service.removeTransPattern(pattern=cucm_variable_axl['pattern'],routePartitionName=cucm_variable_axl['routePartitionName'])
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['UUID','pattern','routePartitionName'])
        csp_table.add_row([result['return'][:],cucm_variable_axl['pattern'], cucm_variable_axl['routePartitionName'] ])
        csp_table_response = csp_table.get_string(fields=['UUID','pattern','routePartitionName'], sortby="UUID").encode('latin-1')
        return {'Status':True,'Detail':csp_table_response}
'''
'''
def Update(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Update(logger,csp_soap_client,cucm_variable_axl)
    # *
    # * Copyright (C) 2016 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    # Mandatory (pattern,usage,routePartitionName)
'''