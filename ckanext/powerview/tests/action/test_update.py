from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin, Resource

from ckanext.powerview.tests import TestBase, factories


class TestUpdatePowerView(TestBase):

    def test_powerview_update(self):
        '''Updating with valid data_dict.'''
        sysadmin = Sysadmin()

        powerview_dict_create = factories.PowerView()

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

        powerview_dict = factories.PowerView()
        powerview_dict['title'] = "New Title"

        powerview_dict_update = toolkit.get_action('powerview_update')(
            context={'user': sysadmin['name']},
            data_dict=powerview_dict
        )

        nosetools.assert_equal(powerview_dict_update['title'],
                               powerview_dict['title'])

    def test_powerview_update_resources_unchanged(self):
        '''Updating a powerview containing resources, leaves them unchanged.'''

        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()
        r3 = Resource()
        resource_id_list = [r1['id'], r2['id'], r3['id']]

        # powerview with resources
        powerview_dict = factories.PowerView(resources=resource_id_list)
        # Update dict with new title
        powerview_dict['title'] = "New Title"

        powerview_dict_update = toolkit.get_action('powerview_update')(
            context={'user': sysadmin['name']},
            data_dict=powerview_dict
        )

        nosetools.assert_equal(set(resource_id_list),
                               set(powerview_dict_update['resources']))

    def test_powerview_update_resources_changed(self):
        '''Updating a powerview's resources, returns expected list in dict.'''

        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()
        r3 = Resource()
        r4 = Resource()
        resource_id_list = [r1['id'], r2['id'], r3['id']]
        updated_resource_id_list = [r1['id'], r3['id'], r4['id']]

        # powerview with resources
        powerview_dict = factories.PowerView(resources=resource_id_list)
        # Update dict with new resource list
        powerview_dict['resources'] = updated_resource_id_list

        powerview_dict_update = toolkit.get_action('powerview_update')(
            context={'user': sysadmin['name']},
            data_dict=powerview_dict
        )

        nosetools.assert_equal(set(updated_resource_id_list),
                               set(powerview_dict_update['resources']))
