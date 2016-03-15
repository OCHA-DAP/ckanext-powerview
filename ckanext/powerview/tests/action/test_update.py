from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin

from ckanext.powerview.tests import TestBase


class TestUpdatePowerView(TestBase):

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

    def test_powerview_update(self):
        '''Updating with valid data_dict.'''
        sysadmin = Sysadmin()

        powerview_dict_create = self._make_powerview(sysadmin)

        powerview_dict_update = toolkit.get_action('powerview_update')(
            context={'user': sysadmin['name']},
            data_dict=powerview_dict_create.copy()
        )

        # last_modified has changed
        nosetools.assert_true(powerview_dict_create['last_modified'] is None)
        nosetools.assert_true(powerview_dict_update['last_modified']
                              is not None)
        # but it should be the only thing that changed
        powerview_dict_update['last_modified'] = None
        nosetools.assert_equal(powerview_dict_create, powerview_dict_update)

    def test_powerview_update_title(self):
        '''Update a powerview with a title.'''
        sysadmin = Sysadmin()

        powerview_dict = self._make_powerview(sysadmin)
        powerview_dict['title'] = "New Title"

        powerview_dict_update = toolkit.get_action('powerview_update')(
            context={'user': sysadmin['name']},
            data_dict=powerview_dict
        )

        nosetools.assert_equal(powerview_dict_update['title'],
                               powerview_dict['title'])
