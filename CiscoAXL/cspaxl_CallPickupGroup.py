# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_DevicePool.py
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

    # Mandatory (name,dateTimeSettingName, callManagerGroupName, regionName, srstName, aarNeighborhoodName, location)
    logger.debug('Se ha entrado en la funcion Add del archivo cspaxl_CallPickupGroup.py')
    axl_cucm = {}
    axl_cucm['pattern'] = '#' + cucm_variable_axl['SiteID']
    axl_cucm['name'] = 'CPG_OF' + cucm_variable_axl['SiteID']
    if len(cucm_variable_axl['routePartitionName'].split('|')) == 1:
        logger.info('Tenemos una sola Partition en el registro')
        axl_cucm['routePartitionName'] = cucm_variable_axl['routePartitionName']
    else:
        logger.info('Tenemos mas de una Partition en el registro')
        P = cucm_variable_axl['routePartitionName'].split('|')
        axl_cucm['routePartitionName'] = P[0]
    
    # Limitamos el numero de caracteres de las variables
    axl_cucm['pattern'] = axl_cucm['pattern'][:50]
    axl_cucm['name'] = axl_cucm['name'][:50]

    # Damos de alta el Device Pool
    try:
        result = csp_soap_client.addCallPickupGroup(axl_cucm)
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
    else:
        csp_table = PrettyTable(['UUID','Call Pickup Group'])
        csp_table.add_row([result['return'][:],axl_cucm['name'] ])
        csp_table_response = csp_table.get_string(fields=['UUID','Call Pickup Group'], sortby="UUID").encode('latin-1')
        logger.info('Result:\n%s' % (csp_table_response.decode("utf-8")))
        return {'Status':True,'Detail':csp_table_response}

def Get(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Get(logger,csp_soap_client,cucm_variable_axl)
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

    # Mandatory (pattern,usage,routePartitionName)
    logger.debug('Se ha entrado en la funcion Get del archivo cspaxl_CallPickupGroup.py')
    try:
        result = csp_soap_client.getCallPickupGroup(name='CPG_OF'+cucm_variable_axl['SiteID'])
    except Fault as err:
        logger.error('ERROR: %s' % (err))
        return {'Status': False, 'Detail': err}
    else:
        logger.info('Result:\n%s' % (result))
        return {'Status':True,'Detail':result}

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