from pydantic import BaseModel
from typing import Literal, Optional

valid_resource_types = [ # TODO: remove this duplication
    'Microsoft.Synapse/workspaces/pipelines',
    'Microsoft.Synapse/workspaces/triggers',
    'Microsoft.Synapse/workspaces/sqlscripts',
    'Microsoft.Synapse/workspaces/managedVirtualNetworks',
    'Microsoft.Synapse/workspaces/linkedservices',
    'Microsoft.Synapse/workspaces/integrationRuntimes',
    'Microsoft.Synapse/workspaces/datasets',
    'Microsoft.Synapse/workspaces/credentials',
]

class Resource(BaseModel):
    type: Optional[Literal[
        'Microsoft.Synapse/workspaces/pipelines',
        'Microsoft.Synapse/workspaces/triggers',
        'Microsoft.Synapse/workspaces/sqlscripts',
        'Microsoft.Synapse/workspaces/managedVirtualNetworks',
        'Microsoft.Synapse/workspaces/linkedservices',
        'Microsoft.Synapse/workspaces/integrationRuntimes',
        'Microsoft.Synapse/workspaces/datasets',
        'Microsoft.Synapse/workspaces/credentials',
    ]]
    raw: dict
    # TODO: other properties such as parent, subscription, etc?