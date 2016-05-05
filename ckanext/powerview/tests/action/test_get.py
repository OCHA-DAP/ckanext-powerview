from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import (Sysadmin,
                                         User,
                                         Resource,
                                         Organization,
                                         Dataset)

from ckanext.powerview.tests import TestBase, factories


class TestShowPowerView(TestBase):

    def test_powerview_show(self):
        '''Calling powerview show with valid id.'''
        sysadmin = Sysadmin()

        powerview_dict_create = factories.PowerView()

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

        powerview_dict_create = factories.PowerView(resources=[r1['id'],
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

    def test_powerview_show_with_private_resource_not_authorized(self):
        '''Calling powerview_show will raise NotAuthorized if powerview
        contains a private resource for user.'''
        org = Organization()
        user = User()
        dataset = Dataset(owner_org=org['id'], private="true")
        r1 = Resource(package_id=dataset['id'])
        r2 = Resource(package_id=dataset['id'])

        p1 = factories.PowerView(private=False,
                                 resources=[r1['id'],
                                            r2['id']])

        powerview_show_action = toolkit.get_action('powerview_show')
        context = {'user': user['name']}
        nosetools.assert_raises(toolkit.NotAuthorized, powerview_show_action,
                                context=context, data_dict={'id': p1['id']})

    def test_powerview_show_with_private_resource_authorized(self):
        '''Calling powerview_show will not raise NotAuthorized if powerview
        contains a private resource for user who is authed to view.'''
        user = User()
        org = Organization(users=[{'name': user['name'],
                                   'capacity': 'member'}])
        dataset = Dataset(owner_org=org['id'], private="true")
        r1 = Resource(package_id=dataset['id'])
        r2 = Resource(package_id=dataset['id'])

        p1 = factories.PowerView(private=False,
                                 resources=[r1['id'],
                                            r2['id']])

        powerview_dict_show = toolkit.get_action('powerview_show')(
            context={'user': user['name']},
            data_dict={'id': p1['id']}
        )
        nosetools.assert_equal(powerview_dict_show, p1)


class TestPowerViewResourceList(TestBase):

    '''Tests for powerview_resource_list'''

    def test_powerview_resource_list_no_resources(self):
        '''
        Calling powerview_resource_list with a powerview that has no resources
        returns an empty list.
        '''
        sysadmin = Sysadmin()

        powerview_dict = factories.PowerView()

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

        powerview = factories.PowerView(resources=[r1['id'],
                                                   r2['id'],
                                                   r3['id']])

        resource_list = toolkit.get_action('powerview_resource_list')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview['id']}
        )

        nosetools.assert_true(r1 in resource_list)
        nosetools.assert_true(r2 in resource_list)
        nosetools.assert_true(r3 in resource_list)


class TestPowerViewList(TestBase):

    '''Tests for powerview_list action'''

    def test_powerview_list_no_powerviews(self):
        '''
        Calling powerview_list when site has no powerviews returns an empty
        list.
        '''
        powerview_list = toolkit.get_action('powerview_list')(data_dict={})
        nosetools.assert_equal(powerview_list, [])

    def test_powerview_list_anon_user(self):
        '''
        Calling powerview_list with an anon user won't show private powerviews.
        '''
        p1 = factories.PowerView(private=True)
        p2 = factories.PowerView(private=False)
        p3 = factories.PowerView(private=False)

        powerview_list = toolkit.get_action('powerview_list')(data_dict={})
        nosetools.assert_equal(len(powerview_list), 2)
        nosetools.assert_true(p1 not in powerview_list)
        nosetools.assert_true(p2 in powerview_list)
        nosetools.assert_true(p3 in powerview_list)

    def test_powerview_list_normal_authorized_user(self):
        '''
        Calling powerview_list with a normal user, who is authorized to view a
        private powerviews, will have it listed.
        '''
        user = User()
        p1 = factories.PowerView(user=user, private=True)
        factories.PowerView(private=False)
        factories.PowerView(private=False)

        context = {'user': user['name']}
        powerview_list = toolkit.get_action('powerview_list')(context,
                                                              data_dict={})
        nosetools.assert_equal(len(powerview_list), 3)
        nosetools.assert_true(p1 in powerview_list)

    def test_powerview_list_with_powerview_with_private_resource(self):
        '''
        Calling powerview_list when a powerview contains a private resource,
        won't have that powerview listed for unauthed user.
        '''
        org = Organization()
        user = User()
        dataset = Dataset(owner_org=org['id'], private="true")
        r1 = Resource(package_id=dataset['id'])
        r2 = Resource(package_id=dataset['id'])

        factories.PowerView(private=False, resources=[r1['id'], r2['id']])

        context = {'user': user['name']}
        powerview_list = toolkit.get_action('powerview_list')(context,
                                                              data_dict={})
        nosetools.assert_equal(powerview_list, [])
