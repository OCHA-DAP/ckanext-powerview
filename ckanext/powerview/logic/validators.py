from ckan.plugins import toolkit

from ckantoolkit import Invalid, _

from ckanext.powerview.model import PowerView


resource_id_exists = toolkit.get_validator('resource_id_exists')


def powerview_id_exists(value, context):
    session = context['session']

    result = session.query(PowerView).get(value)
    if not result:
        raise Invalid('%s: %s' % (_('Not found'), _('PowerView')))
    return value


def resource_ids_in_list(value, context):
    '''Validate resource id list.'''

    # value must be a list
    if not isinstance(value, list):
        raise Invalid(_('Not a list'))

    for i in value:
        # item must be a string
        if not isinstance(i, basestring):
            raise Invalid('%s: %s' % (_('Not a string'), i))

        # item must be a resource id that exists
        resource_id_exists(i, context)

    return value
