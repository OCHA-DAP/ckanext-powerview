import datetime

from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema
from ckanext.powerview.model import PowerView

import logging
log = logging.getLogger(__name__)


@validate(schema.powerview_update_schema)
def powerview_update(context, data_dict):
    '''Update an existing powerview.

    You must provide your API key in the Authorization header.

    '''

    toolkit.check_access('ckanext_powerview_update', context, data_dict)

    powerview = PowerView.get(id=data_dict['id'])

    ignored_keys = ['id', 'created', 'last_modified']

    for k, v in data_dict.items():
        if k not in ignored_keys:
            setattr(powerview, k, v)

    powerview.last_modified = datetime.datetime.now()

    session = context['session']
    session.add(powerview)
    session.commit()

    return powerview.as_dict()
