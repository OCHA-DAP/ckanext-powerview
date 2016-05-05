import ckan.plugins.toolkit as toolkit

import ckan.model as model

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
    '''
    Checks access to both the powerview, and its contained resources.

    If the user can view the powerview, but can't view one of its resources,
    they won't have access to the powerview.
    '''
    powerview = PowerView.get(id=data_dict['id'])

    if not powerview:
        return {'success': False}

    powerview = powerview.as_dict()
    user = context.get('user')

    # Check resources first
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

    # Resource check okay, so is powerview public?
    if not powerview['private']:
        return {'success': True}
    elif user:
        # Private powerview, so check user has permission
        user_obj = model.User.get(user)

        authorized = user_has_permission_for_powerview(user_obj, powerview)

        if authorized:
            return {'success': True}
        else:
            return {
                'success': False,
                'msg': _('User {0} not authorized to read powerview {1}'
                         .format(user, powerview['id']))}

    # powerview is private and there's no user
    return {'success': False}


@toolkit.auth_allow_anonymous_access
def resource_list(context, data_dict):
    '''List resources in a powerview.

    If a user doesn't have permission to view a resource contained by the
    powerview, they won't be authorized.

    Resource access is checked as part of powerview_show auth, so call it.
    '''
    return show(context, data_dict)


@toolkit.auth_allow_anonymous_access
def powerview_list(context, data_dict):
    '''List of powerviews accessible by user.'''
    # PowerView list is visible by default.
    # Exactly which PowerViews will be listed if defined by the action.
    return {'success': True}


def user_has_permission_for_powerview(user, powerview_dict):
    '''Return True if user has permission to view powerview.

    If private, only the creator can view the powerview, but may include
    organization checks here in the future.
    '''

    if (not powerview_dict['private'] or
       powerview_dict['created_by'] == user.id):
        return True
    else:
        return False
