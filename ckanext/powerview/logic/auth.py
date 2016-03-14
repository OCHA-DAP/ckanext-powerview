import ckan.plugins.toolkit as toolkit


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
    '''All users can access a PowerView show.'''
    return {'success': True}
