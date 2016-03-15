import ckan.model as model
from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema
from ckanext.powerview.model import PowerView

import logging
log = logging.getLogger(__name__)


@validate(schema.powerview_create_schema)
def powerview_create(context, data_dict):
    '''Create a new powerview.

    You must provide your API key in the Authorization header.

    '''
    toolkit.check_access('ckanext_powerview_create', context, data_dict)

    user = context['user']
    user_obj = model.User.get(user)
    data_dict['created_by'] = user_obj.id

    powerview = PowerView(**data_dict)

    session = context['session']
    session.add(powerview)
    session.commit()

    return powerview.as_dict()
