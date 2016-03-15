from ckantoolkit import Invalid, _

from ckanext.powerview.model import PowerView


def powerview_id_exists(value, context):
    session = context['session']

    result = session.query(PowerView).get(value)
    if not result:
        raise Invalid('%s: %s' % (_('Not found'), _('PowerView')))
    return value
