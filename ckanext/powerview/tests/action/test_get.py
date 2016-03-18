from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin, Resource

from ckanext.powerview.tests import TestBase


def _make_powerview(user, resources=None):
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


class TestShowPowerView(TestBase):

    def test_powerview_show(self):
        '''Calling powerview show with valid id.'''
        sysadmin = Sysadmin()

        powerview_dict_create = _make_powerview(sysadmin)

        powerview_dict_show = toolkit.get_action('powerview_show')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict_create['id']}
        )

        nosetools.assert_equal(powerview_dict_create, powerview_dict_show)

    def test_powerview_show_with_resources(self):
        '''Calling powerview show should return list of resource ids.'''
        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()
        r3 = Resource()

        powerview_dict_create = _make_powerview(sysadmin,
                                                [r1['id'],
                                                 r2['id'],
                                                 r3['id']])

        powerview_dict_show = toolkit.get_action('powerview_show')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict_create['id']}
        )

        nosetools.assert_equal(powerview_dict_create, powerview_dict_show)
        resource_list = powerview_dict_show['resources']
        nosetools.assert_equal(len(resource_list), 3)
        nosetools.assert_true(r1['id'] in resource_list)
        nosetools.assert_true(r2['id'] in resource_list)
        nosetools.assert_true(r3['id'] in resource_list)


class TestPowerViewResourceList(TestBase):

    '''Tests for powerview_resource_list'''

    def test_powerview_resource_list_no_resources(self):
        '''
        Calling powerview_resource_list with a power that has no resources
        returns an empty list.
        '''
        sysadmin = Sysadmin()

        powerview_dict = _make_powerview(sysadmin)

        resource_list = toolkit.get_action('powerview_resource_list')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict['id']}
        )

        nosetools.assert_equal(resource_list, [])

    def test_powerview_resource_list_with_resources(self):
        '''
        Calling powerview_resource_list with a powerview that has resources
        should return them.
        '''
        sysadmin = Sysadmin()
        r1 = Resource()
        r2 = Resource()
        r3 = Resource()

        powerview = _make_powerview(sysadmin, resources=[r1['id'],
                                                         r2['id'],
                                                         r3['id']])

        resource_list = toolkit.get_action('powerview_resource_list')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview['id']}
        )

        nosetools.assert_true(r1 in resource_list)
        nosetools.assert_true(r2 in resource_list)
        nosetools.assert_true(r3 in resource_list)
