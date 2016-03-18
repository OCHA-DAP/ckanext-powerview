import ckan.plugins.toolkit as toolkit

import ckan.model as model
from ckan.new_authz import is_authorized as ckan_is_authorized

from ckantoolkit import _, NotAuthorized

from ckanext.powerview.model import PowerView


def create(context, data_dict):
    '''Create a PowerView.

       Only sysadmins can create a PowerView.
    '''
    return {'success': False}


def delete(context, data_dict):
    '''Delete a PowerView.

       Only sysadmins can delete a PowerView.
    '''
    return {'success': False}


def update(context, data_dict):
    '''Update a PowerView.

       Only sysadmins can update a PowerView.
    '''
    return {'success': False}


@toolkit.auth_allow_anonymous_access
def show(context, data_dict):
    '''All users can view public PowerViews.'''

    powerview = PowerView.get(id=data_dict['id'])

    # If public, just allow
    if powerview and not powerview.private:
        return {'success': True}

    # So we haven't got a powerview or it's private...

    user = context.get('user')

    if powerview and user:
        user_obj = model.User.get(user)

        authorized = _user_has_permission_for_powerview(user_obj, powerview)

        if authorized:
            return {'success': True}
        else:
            return {
                'success': False,
                'msg': _('User {0} not authorized to read powerview {1}'
                         .format(user, powerview.id))}
    else:
        return {'success': False}


@toolkit.auth_allow_anonymous_access
def resource_list(context, data_dict):
    '''List resources in a powerview.

    If a user hasn't got permission to view a resource contained by the
    powerview, they won't be authorized.
    '''
    user = context.get('user')

    powerview = toolkit.get_action('powerview_show')(
        context=context,
        data_dict={'id': data_dict['id']}
    )

    if not powerview:
        return {'success': False}

    # check authentication against each resource
    for res_id in powerview['resources']:
        try:
            toolkit.check_access('resource_show', context,
                                 data_dict={'id': res_id})
        except NotAuthorized:
            return {
                'success': False,
                'msg': _('User {0} not authorized to read resource {1}'
                         .format(user, res_id))
            }

    return {'success': True}


def _user_has_permission_for_powerview(user, powerview):
    '''Return True if user has permission to view powerview.

    If private, only the creator can view the powerview, but may include
    organization checks here in the future.
    '''

    if not powerview.private or powerview.created_by == user.id:
        return True
    else:
        return False
