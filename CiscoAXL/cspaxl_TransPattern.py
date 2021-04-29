# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_TransPattern.py
# *
# * Cisco AXL Python
# *
# * Copyright (C) 2015 Carlos Sanz <carlos.sanzpenas@gmail.com>
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
from prettytable import PrettyTable
from zeep.exceptions import Fault

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

    # Mandatory (pattern,usage,routePartitionName)
    #axl_cucm = cucm_variable_axl
    axl_cucm = {}
    if cucm_variable_axl['DID'][0] == '+':
        axl_cucm['pattern'] = '\\' + cucm_variable_axl['DID']
    elif cucm_variable_axl['DID'][0] == '0':
        axl_cucm['pattern'] = cucm_variable_axl['DID']
    else:
        axl_cucm['pattern'] = '0' + cucm_variable_axl['DID']
    axl_cucm['description'] = 'DDI Entrante Oficina ' + cucm_variable_axl['SiteID'] + ' ORANGE'

    if len(cucm_variable_axl['DirectoryNumber'].split('|')) == 1:
        logger.info('Tenemos una solo Directory Number en el registro')
        axl_cucm['calledPartyTransformationMask'] = cucm_variable_axl['DirectoryNumber']
    else:
        logger.info('Tenemos mas de un Directory Number en el registro')
        DN = cucm_variable_axl['DirectoryNumber'].split('|')
        axl_cucm['calledPartyTransformationMask'] = DN[0]


    axl_cucm['callingSearchSpaceName'] = cucm_variable_axl['CallingSearchSpace']

    if len(cucm_variable_axl['routePartitionName'].split('|')) == 1:
        logger.info('Tenemos una sola Partition en el registro')
        axl_cucm['routePartitionName'] = cucm_variable_axl['routePartitionName']
    else:
        logger.info('Tenemos mas de una Partition en el registro')
        P = cucm_variable_axl['routePartitionName'].split('|')
        axl_cucm['routePartitionName'] = P[0]

    axl_cucm['usage'] = 'Translation'
    axl_cucm['patternUrgency'] = 'true'
    axl_cucm['provideOutsideDialtone'] = 'false'

    # Comprobamos que el Translation Pattern no existe
    try:
        csp_soap_returnedTags = {'pattern': '', 'routePartitionName': ''}
        csp_soap_searchCriteria = {'pattern': axl_cucm['pattern'],'routePartitionName':axl_cucm['routePartitionName']}
        result = csp_soap_client.listTransPattern(csp_soap_searchCriteria,csp_soap_returnedTags)
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}

    else:
        if (result['return'] is None):
            logger.info('El Translation Pattern %s en la Partition %s no existe en el CUCM' % (axl_cucm['pattern'],axl_cucm['routePartitionName']))
        else:
            logger.info('El Translation Pattern %s en la Partition %s existe en el CUCM' % (axl_cucm['pattern'],axl_cucm['routePartitionName']))
            return {'Status': False, 'Detail': axl_cucm['pattern']}

    # Damos de alta el Translation Pattern
    try:
        result = csp_soap_client.addTransPattern(axl_cucm)
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
    else:
        csp_table = PrettyTable(['UUID','pattern','routePartitionName'])
        csp_table.add_row([result['return'][:],axl_cucm['pattern'], axl_cucm['routePartitionName'] ])
        csp_table_response = csp_table.get_string(fields=['UUID','pattern','routePartitionName'], sortby="UUID").encode('latin-1')
        logger.info('Result:\n%s' % (csp_table_response.decode("utf-8")))
        return {'Status': True,'Detail':csp_table_response}

def Get(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Get(logger,csp_soap_client,cucm_variable_axl)
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
        #result = csp_soap_client.service.getTransPattern(pattern='',cucm_variable_axl)
        result = csp_soap_client.getTransPattern({'uuid': 'a7bacb02-b820-85a9-ca53-6bbfce94c9c9'})
        #result = csp_soap_client.service.getTransPattern(pattern='17150',routePartitionName='INTERNA')
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
    else:
        print (result)
        #csp_table = PrettyTable(['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'])
        #csp_table.add_row([0,result['return']['processNode']['name'],result['return']['processNode']['description'],result['return']['processNode']['mac'],result['return']['processNode']['ipv6Name'],result['return']['processNode']['nodeUsage'],result['return']['processNode']['lbmHubGroup'],result['return']['processNode']['processNodeRole'] ])
        #csp_table_response = csp_table.get_string(fields=['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'], sortby="id").encode('latin-1')
        return {'Status':True,'Detail':csp_table_response}

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
    returnedTags = {'pattern':'','routePartitionName':'','calledPartyTransformationMask':'','callingSearchSpaceName':''}
    searchCriteria = {'pattern': '%' + cucm_variable_axl + '%'}

    try:
        result = csp_soap_client.service.listTransPattern(searchCriteria,returnedTags)
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
    else:
        csp_table = PrettyTable(['id','pattern','routePartitionName','callingSearchSpaceName','calledPartyTransformationMask'])
        for x in range(0, len(result['return']['transPattern'])):
            csp_table.add_row([x,result['return']['transPattern'][x]['pattern'],result['return']['transPattern'][x]['routePartitionName']['value'],result['return']['transPattern'][x]['callingSearchSpaceName']['value'],result['return']['transPattern'][x]['calledPartyTransformationMask'] ])

        csp_table_response = csp_table.get_string(fields=['id','pattern','routePartitionName','callingSearchSpaceName','calledPartyTransformationMask'], sortby="id").encode('latin-1')
        logger.debug ('Los Translation Pattern encontrados son: \n\n%s\n' % (str(csp_table_response,'utf-8')))
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