from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema
from ckanext.powerview.model import PowerView

import logging
log = logging.getLogger(__name__)


@toolkit.side_effect_free
@validate(schema.powerview_show_schema)
def powerview_show(context, data_dict):
    '''Show an existing powerview.

    :param id: the id of the powerview to show
    :type id: string

    '''

    toolkit.check_access('ckanext_powerview_show', context, data_dict)

    powerview = PowerView.get(id=data_dict['id'])

    return powerview.as_dict()
