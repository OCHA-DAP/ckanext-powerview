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

    :param title: title of the powerview
    :type title: string
    :param description: a description for the powerview
    :type description: string
    :param view_type: type of view
    :type view_type: string
    :param resources: resource ids available for this view
    :type resources: list
    :param config: options necessary to recreate a view state
    :type config: JSON string
    :param owner_org: id of the owning organization
    :type owner_org: string
    :param private: determines if view is publicly accessible
    :type private: boolean

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
