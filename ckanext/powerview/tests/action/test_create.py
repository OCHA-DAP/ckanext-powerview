from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin, Resource

from ckanext.powerview.tests import TestBase
from ckanext.powerview.model import PowerviewResourceAssociation


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
        # created_by field auto-populated
        nosetools.assert_equal(powerview_result['created_by'], sysadmin['id'])

    def test_powerview_create_private_defaults_to_false(self):
        '''private will default to False when not specified.'''

        sysadmin = Sysadmin()

        create_dict = self._make_create_data_dict()
        del create_dict['private']

        powerview_result = toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=create_dict
        )

        nosetools.assert_false(powerview_result['private'])

    def test_powerview_create_resource_id_list_creates_associations(self):
        '''If resource id list is provided, associations are create with
        powerview.'''
        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()
        r3 = Resource()

        create_dict = self._make_create_data_dict()
        create_dict['resources'] = [r1['id'], r2['id'], r3['id']]

        toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=create_dict
        )

        nosetools.assert_equal(PowerviewResourceAssociation.count(), 3)

    def test_powerview_create_resource_id_list_contains_duplicates(self):
        '''Resource id list is de-duplicated before associations are
        created.'''
        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()

        create_dict = self._make_create_data_dict()
        # r2 id added twice
        create_dict['resources'] = [r1['id'], r2['id'], r2['id']]

        toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=create_dict
        )

        nosetools.assert_equal(PowerviewResourceAssociation.count(), 2)
