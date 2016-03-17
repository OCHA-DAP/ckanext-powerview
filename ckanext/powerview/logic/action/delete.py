from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema
from ckanext.powerview.model import PowerView, PowerviewResourceAssociation

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
    powerview.delete()
    session.commit()


@validate(schema.powerview_resource_association_delete_schema)
def powerview_remove_resource(context, data_dict):
    '''Remove a resource id to an existing powerview.

    You must provide your API key in the Authorization header.

    :param id: id of the powerview
    :type id: string
    :param resource_id: id of the resource to add
    :type resource_id: string

    '''
    toolkit.check_access('ckanext_powerview_delete', context, data_dict)

    resource_id = data_dict['resource_id']
    powerview_id = data_dict['id']

    if not PowerviewResourceAssociation.exists(resource_id=resource_id,
                                               powerview_id=powerview_id):
        raise toolkit.ValidationError("Resource not associated with powerview.",
                                      error_summary=u"The resource, {0}, is not in the powerview".format(resource_id))

    assoc = PowerviewResourceAssociation.get(resource_id=resource_id,
                                             powerview_id=powerview_id)
    session = context['session']
    assoc.delete()
    session.commit()
