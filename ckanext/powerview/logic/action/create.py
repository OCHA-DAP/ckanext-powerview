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

    :param title: title of the powerview
    :type title: string
    :param description: a description for the powerview (optional)
    :type description: string
    :param view_type: type of view
    :type view_type: string
    :param resources: resource ids available for this view (optional)
    :type resources: list
    :param config: options necessary to recreate a view state (optional)
    :type config: JSON string
    :param owner_org: id of the owning organization (optional)
    :type owner_org: string
    :param private: determines if view is publicly accessible (optional,
        defaults to False)
    :type private: boolean

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
