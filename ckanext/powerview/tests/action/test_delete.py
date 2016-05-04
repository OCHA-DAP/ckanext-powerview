from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit
import ckan.model as model

from ckantoolkit import ValidationError
from ckantoolkit.tests.factories import Sysadmin, Resource

from ckanext.powerview.tests import TestBase, factories
from ckanext.powerview.model import PowerView, PowerviewResourceAssociation


class TestDeletePowerView(TestBase):

    def test_powerview_delete(self):
        '''Calling powerview delete with valid data_dict.'''
        sysadmin = Sysadmin()

        powerview_dict = factories.PowerView()

        # one powerview
        nosetools.assert_equal(PowerView.count(), 1)

        toolkit.get_action('powerview_delete')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict['id']}
        )

        # No powerview
        nosetools.assert_equal(PowerView.count(), 0)

    def test_powerview_delete_with_resources(self):
        '''Calling powerview delete also removes resource association
        objects, but leaves Resources intact.'''

        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()
        r3 = Resource()
        resource_id_list = [r1['id'], r2['id'], r3['id']]

        powerview_dict = factories.PowerView(resources=resource_id_list)

        # one powerview
        nosetools.assert_equal(PowerView.count(), 1)
        nosetools.assert_equal(PowerviewResourceAssociation.count(), 3)
        nosetools.assert_equal(
            model.meta.Session.query(model.Resource).count(), 3)

        toolkit.get_action('powerview_delete')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict['id']}
        )

        # No powerview
        nosetools.assert_equal(PowerView.count(), 0)
        nosetools.assert_equal(PowerviewResourceAssociation.count(), 0)
        # Still have the resources
        nosetools.assert_equal(
            model.meta.Session.query(model.Resource).count(), 3)


class TestPowerviewRemoveResource(TestBase):

    def test_powerview_remove_resource_valid(self):
        sysadmin = Sysadmin()
        r1 = Resource()

        powerview_dict = factories.PowerView(resources=[r1['id']])

        nosetools.assert_equal(PowerviewResourceAssociation.count(), 1)

        toolkit.get_action('powerview_remove_resource')(
            context={'user': sysadmin['name']},
            data_dict={
                'id': powerview_dict['id'],
                'resource_id': r1['id']
            }
        )

        nosetools.assert_equal(PowerviewResourceAssociation.count(), 0)

    def test_powerview_remove_resource_unassociated_resource(self):
        '''Calling powerview_remove_resource with an unassociated resource id
        raises an error.'''
        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()

        powerview_dict = factories.PowerView(resources=[r1['id']])

        with nosetools.assert_raises(ValidationError):
            toolkit.get_action('powerview_remove_resource')(
                context={'user': sysadmin['name']},
                data_dict={
                    'id': powerview_dict['id'],
                    'resource_id': r2['id']
                }
            )

    def test_powerview_remove_resource_retains_objects(self):
        '''Calling powerview_remove_resource doesn't delete powerview or
        resource.'''
        sysadmin = Sysadmin()
        r1 = Resource()

        powerview_dict = factories.PowerView(resources=[r1['id']])

        nosetools.assert_equal(PowerView.count(), 1)
        nosetools.assert_equal(
            model.meta.Session.query(model.Resource).count(), 1)

        toolkit.get_action('powerview_remove_resource')(
            context={'user': sysadmin['name']},
            data_dict={
                'id': powerview_dict['id'],
                'resource_id': r1['id']
            }
        )

        nosetools.assert_equal(PowerView.count(), 1)
        nosetools.assert_equal(
            model.meta.Session.query(model.Resource).count(), 1)

    def test_powerview_remove_resource_no_longer_in_resource_list(self):
        '''Calling powerview_remove_resource removes resource id from
        powerview resource list.'''
        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()

        powerview_dict = factories.PowerView(resources=[r1['id'], r2['id']])

        toolkit.get_action('powerview_remove_resource')(
            context={'user': sysadmin['name']},
            data_dict={
                'id': powerview_dict['id'],
                'resource_id': r1['id']
            }
        )

        updated_dict = toolkit.get_action('powerview_show')(
            context={'user': sysadmin['name']},
            data_dict={
                'id': powerview_dict['id']
            }
        )

        nosetools.assert_equal(updated_dict['resources'], [r2['id']])
