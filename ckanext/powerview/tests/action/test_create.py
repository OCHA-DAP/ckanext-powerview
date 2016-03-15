from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin

from ckanext.powerview.tests import TestBase


class TestCreatePowerView(TestBase):

    def _make_create_data_dict(self):
        data_dict = {
            'title': 'Title',
            'description': 'My short description.',
            'view_type': 'my-view-type',
            'config': '{"my":"json"}',
            'private': 'yes'
        }
        return data_dict

    def test_powerview_create(self):
        '''Creating a powerview returns a dict with expected values'''
        sysadmin = Sysadmin()

        powerview_result = toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=self._make_create_data_dict()
        )

        nosetools.assert_true(isinstance(powerview_result, dict))
        nosetools.assert_true(powerview_result['title'] == 'Title')
        nosetools.assert_true(powerview_result['description'] ==
                              'My short description.')
        nosetools.assert_true(powerview_result['view_type'] == 'my-view-type')
        nosetools.assert_true(isinstance(powerview_result['config'], dict))
        nosetools.assert_true(powerview_result['private'])
