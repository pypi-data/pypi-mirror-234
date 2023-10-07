import logging
from pipedocs.models import Resource, valid_resource_types
from typing import List
logger = logging.getLogger(__name__)


type_to_parser = [ # TODO: remove this duplication
    'Microsoft.Synapse/workspaces/pipelines',
    'Microsoft.Synapse/workspaces/triggers',
    'Microsoft.Synapse/workspaces/sqlscripts',
    'Microsoft.Synapse/workspaces/managedVirtualNetworks',
    'Microsoft.Synapse/workspaces/linkedservices',
    'Microsoft.Synapse/workspaces/integrationRuntimes',
    'Microsoft.Synapse/workspaces/datasets',
    'Microsoft.Synapse/workspaces/credentials',
]

class Documenter():
    def document(self, pipelines: List[dict]) -> str:
        pass

    def parse_resource(self, resource_raw: dict) -> Resource:
        type = None
        if ('type' in resource_raw) and (resource_raw['type'] in valid_resource_types):
            type = resource_raw['type']
        elif ('properties' in resource_raw) and ('type' in resource_raw['properties']):
            if resource_raw['properties']['type'] == 'SqlQuery':
                type = 'Microsoft.Synapse/workspaces/sqlscripts'
        else:
            #logging.warning('Could not parse resource')
            pass


        return Resource(
            type = type,
            raw = resource_raw
        )

