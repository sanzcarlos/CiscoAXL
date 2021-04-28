# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_Line.py
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
import re
from unicodedata import normalize
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

    # Mandatory (pattern,usage)
    logger.debug('Se ha entrado en la funcion Add del archivo cspaxl_Line.py')
    axl_cucm = {}
    axl_cucm['pattern'] = cucm_variable_axl['DirectoryNumber']
    axl_cucm['usage'] = 'Device'
    axl_cucm['callPickupGroupName'] = cucm_variable_axl['callPickupGroupName']
    axl_cucm['routePartitionName'] = cucm_variable_axl['routePartitionName']
    axl_cucm['description'] = cucm_variable_axl['UserFirstName'] + ' ' + cucm_variable_axl['UserSurname']
    axl_cucm['alertingName'] = axl_cucm['description']
    axl_cucm['asciiAlertingName'] = String2ASCI(logger,axl_cucm['alertingName'])
    axl_cucm['voiceMailProfileName'] = cucm_variable_axl['voiceMailProfileName']

    # Rellenamos todos los Permisos para los desvios
    axl_cucm['shareLineAppearanceCssName'] = cucm_variable_axl['CallingSearchSpace']
    axl_cucm['callForwardAll'] = {'destination': '',
                                  'forwardToVoiceMail': 'false',
                                  'callingSearchSpaceName': cucm_variable_axl['CSSForward'],
                                  'secondaryCallingSearchSpaceName': cucm_variable_axl['CSSForward']}
    axl_cucm['callForwardBusy'] = {'destination': '',
                                   'forwardToVoiceMail': 'false',
                                   'callingSearchSpaceName': cucm_variable_axl['CSSForward']}
    axl_cucm['callForwardBusyInt'] = axl_cucm['callForwardBusy']
    axl_cucm['callForwardNoAnswer'] = axl_cucm['callForwardBusy']
    axl_cucm['callForwardNoAnswerInt'] = axl_cucm['callForwardBusy']
    axl_cucm['callForwardNoCoverage'] = axl_cucm['callForwardBusy']
    axl_cucm['callForwardNoCoverageInt'] = axl_cucm['callForwardBusy']
    axl_cucm['callForwardOnFailure'] = axl_cucm['callForwardBusy']
    axl_cucm['callForwardNotRegistered'] = axl_cucm['callForwardBusy']
    axl_cucm['callForwardNotRegisteredInt'] = axl_cucm['callForwardBusy']

    # Limitamos el numero de caracteres de las variables
    axl_cucm['alertingName'] = axl_cucm['alertingName'][:50]
    axl_cucm['asciiAlertingName'] = axl_cucm['asciiAlertingName'][:32]
    #axl_cucm['parkMonForwardNoRetrieveDn'] = axl_cucm['parkMonForwardNoRetrieveDn'][:50]
    #axl_cucm['parkMonForwardNoRetrieveIntDn'] = axl_cucm['parkMonForwardNoRetrieveIntDn'][:50]

    # Damos de alta la Linea
    try:
        result = csp_soap_client.addLine(axl_cucm)
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
    else:
        csp_table = PrettyTable(['UUID','Directory Number','routePartitionName'])
        csp_table.add_row([result['return'][:], axl_cucm['pattern'], axl_cucm['routePartitionName']])
        csp_table_response = csp_table.get_string(fields=['UUID', 'Directory Number', 'routePartitionName'],
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

    # Mandatory (pattern,routePartitionName)
    try:
        result = csp_soap_client.getLine(pattern=cucm_variable_axl['DirectoryNumber'],routePartitionName=cucm_variable_axl['routePartitionName'])
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
    else:
        logger.info('Result:\n%s' % (result))
        return {'Status':True,'Detail':result}
'''
def List(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function List(logger,csp_soap_client,cucm_variable_axl)
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
    returnedTags = {'name':'','description':'','mac':'','ipv6Name':'','nodeUsage':'','lbmHubGroup':'','processNodeRole':''}
    searchCriteria = {'name': '%' + cucm_variable_axl + '%'}

    try:
        result = csp_soap_client.service.listProcessNode(searchCriteria,returnedTags)
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
    else:
        csp_table = PrettyTable(['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'])
        for x in range(0, len(result['return']['processNode'])):
            csp_table.add_row([x,result['return']['processNode'][x]['name'],result['return']['processNode'][x]['description'],result['return']['processNode'][x]['mac'],result['return']['processNode'][x]['ipv6Name'],result['return']['processNode'][x]['nodeUsage'],result['return']['processNode'][x]['lbmHubGroup'],result['return']['processNode'][x]['processNodeRole'] ])
        csp_table_response = csp_table.get_string(fields=['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'], sortby="id").encode('latin-1')
        return {'Status':True,'Detail':csp_table_response}
'''
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
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
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