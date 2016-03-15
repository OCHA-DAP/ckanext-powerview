from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin

from ckanext.powerview.tests import TestBase
from ckanext.powerview.model import PowerView


class TestDeletePowerView(TestBase):

    def _make_powerview(self, user):
        '''Make a powerview and return the resulting data_dict.'''
        data_dict = {
            'title': 'Title',
            'description': 'My short description.',
            'view_type': 'my-view-type',
            'config': '{"my":"json"}',
            'private': 'yes'
        }

        return toolkit.get_action('powerview_create')(
            context={'user': user['name']},
            data_dict=data_dict
        )

    def test_powerview_delete(self):
        '''Calling powerview delete with valid data_dict.'''
        sysadmin = Sysadmin()

        powerview_dict_create = self._make_powerview(sysadmin)

        # one powerview
        nosetools.assert_equal(PowerView.count(), 1)

        toolkit.get_action('powerview_delete')(
            context={'user': sysadmin['name']},
            data_dict=powerview_dict_create
        )

        # No powerview
        nosetools.assert_equal(PowerView.count(), 0)
