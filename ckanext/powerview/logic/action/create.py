import ckan.model as model
from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.powerview.logic import schema
from ckanext.powerview.model import PowerView, PowerviewResourceAssociation

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

    for res_id in data_dict.get('resources', []):
        # We validate for id duplication, so this shouldn't be true during
        # create.
        if PowerviewResourceAssociation.exists(powerview_id=powerview.id,
                                               resource_id=res_id):
            raise toolkit.ValidationError("Resource already associated with powerview.",
                                          error_summary=u"The resource, {0}, is already in the powerview".format(res_id))

        # create the association
        PowerviewResourceAssociation.create(resource_id=res_id,
                                            powerview_id=powerview.id)

    return powerview.as_dict()


@validate(schema.powerview_resource_association_create_schema)
def powerview_add_resource(context, data_dict):
    '''Add a resource id to an existing powerview.

    You must provide your API key in the Authorization header.

    :param id: id of the powerview
    :type id: string
    :param resource_id: id of the resource to add
    :type resource_id: string
    '''

    toolkit.check_access('ckanext_powerview_create', context, data_dict)

    powerview_id = data_dict['id']
    resource_id = data_dict['resource_id']

    if PowerviewResourceAssociation.exists(powerview_id=powerview_id,
                                           resource_id=resource_id):
        raise toolkit.ValidationError("Resource already association with powerview.",
                                      error_summary=u"The resource, {0}, is already in the powerview".format(resource_id))

    # create the association
    association = PowerviewResourceAssociation.create(resource_id=resource_id,
                                                      powerview_id=powerview_id)

    return association
