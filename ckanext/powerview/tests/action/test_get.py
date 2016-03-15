from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin

from ckanext.powerview.tests import TestBase


class TestShowPowerView(TestBase):

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

    def test_powerview_show(self):
        '''Calling powerview show with valid id.'''
        sysadmin = Sysadmin()

        powerview_dict_create = self._make_powerview(sysadmin)

        powerview_dict_show = toolkit.get_action('powerview_show')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict_create['id']}
        )

        nosetools.assert_equal(powerview_dict_create, powerview_dict_show)
