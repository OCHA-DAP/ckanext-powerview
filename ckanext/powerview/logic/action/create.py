from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema


@validate(schema.powerview_create_schema)
def powerview_create(context, data_dict):
    '''Create a new powerview.

    You must provide your API key in the Authorization header.


    '''
    # toolkit.check_access('powerview_create', context, data_dict)
    pass
