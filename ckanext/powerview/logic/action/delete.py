from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema
from ckanext.powerview.model import PowerView

import logging
log = logging.getLogger(__name__)


@validate(schema.powerview_delete_schema)
def powerview_delete(context, data_dict):
    '''Delete an existing powerview.

    :param id: the id of the powerview to delete
    :type id: string

    '''

    toolkit.check_access('ckanext_powerview_delete', context, data_dict)

    powerview = PowerView.get(id=data_dict['id'])

    session = context['session']
    powerview.purge()
    session.commit()
