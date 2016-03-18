from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema
from ckanext.powerview.model import PowerView, PowerviewResourceAssociation

import logging
log = logging.getLogger(__name__)


@toolkit.side_effect_free
@validate(schema.powerview_show_schema)
def powerview_show(context, data_dict):
    '''Show an existing powerview.

    :param id: the id of the powerview to show
    :type id: string

    :rtype: dictionary

    '''

    toolkit.check_access('ckanext_powerview_show', context, data_dict)

    powerview = PowerView.get(id=data_dict['id'])

    return powerview.as_dict()


@toolkit.side_effect_free
@validate(schema.powerview_resource_list)
def powerview_resource_list(context, data_dict):
    '''List resources associated with a powerview.

    :param id: id of the powerview
    :type id: string

    :rtype: list of dictionaries
    '''

    toolkit.check_access('ckanext_powerview_resource_list', context, data_dict)

    # get a list of resource ids associated with the powerview id
    resource_id_list = \
        PowerviewResourceAssociation.get_resource_ids_for_powerview(
            data_dict['id'])

    resource_list = []
    if resource_id_list is not None:
        for res_id in resource_id_list:
            resource = toolkit.get_action('resource_show')(context,
                                                           {'id': res_id})
            resource_list.append(resource)

    return resource_list
