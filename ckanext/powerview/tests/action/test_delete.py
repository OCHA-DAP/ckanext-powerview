from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit
import ckan.model as model

from ckantoolkit.tests.factories import Sysadmin, Resource

from ckanext.powerview.tests import TestBase
from ckanext.powerview.model import PowerView, PowerviewResourceAssociation


class TestDeletePowerView(TestBase):

    def _make_powerview(self, user, resources=None):
        '''Make a powerview and return the resulting data_dict.'''
        data_dict = {
            'title': 'Title',
            'description': 'My short description.',
            'view_type': 'my-view-type',
            'config': '{"my":"json"}',
            'private': 'yes'
        }
        if resources:
            data_dict['resources'] = resources

        return toolkit.get_action('powerview_create')(
            context={'user': user['name']},
            data_dict=data_dict
        )

    def test_powerview_delete(self):
        '''Calling powerview delete with valid data_dict.'''
        sysadmin = Sysadmin()

        powerview_dict = self._make_powerview(sysadmin)

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

        powerview_dict = self._make_powerview(sysadmin,
                                              resource_id_list)

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
