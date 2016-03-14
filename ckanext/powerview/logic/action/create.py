from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema

import logging
log = logging.getLogger(__name__)


@validate(schema.powerview_create_schema)
def powerview_create(context, data_dict):
    '''Create a new powerview.

    You must provide your API key in the Authorization header.

    '''
    toolkit.check_access('ckanext_powerview_create', context, data_dict)
