from nose import tools as nosetools

import ckan.model as model

from ckantoolkit.tests import helpers, factories
from ckantoolkit import NotAuthorized

from ckanext.powerview.tests import TestBase
from ckanext.powerview.tests import factories as powerview_factories


class TestPowerViewCreateAuth(TestBase):

    def _make_create_data_dict(self, resources=None):
        data_dict = {
            'title': 'Title',
            'description': 'My short description.',
            'view_type': 'my-view-type',
            'config': '{"my":"json"}',
            'private': 'yes'
        }
        if resources:
            data_dict['resources'] = resources
        return data_dict

    def test_powerview_create_sysadmin(self):
        '''
        Calling powerview create with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        pv_dict = self._make_create_data_dict()
        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_create',
                                                context=context, **pv_dict))

    def test_powerview_create_normal_user(self):
        '''
        Calling powerview create with normal logged in user raises
        NotAuthorized.
        '''
        a_user = factories.User()
        pv_dict = self._make_create_data_dict()
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_create',
                                context=context, **pv_dict)

    def test_powerview_create_anon_user(self):
        '''
        Calling powerview create with anon user raises NotAuthorized.
        '''
        context = {'user': '', 'model': model}
        pv_dict = self._make_create_data_dict()
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_create',
                                context=context, **pv_dict)

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_create_normal_user_allow_create(self):
        '''
        Calling powerview create with normal user when allow_user_create is
        true, doesn't raise NotAuthorized.
        '''
        a_user = factories.User()
        pv_dict = self._make_create_data_dict()
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_create',
                                                context=context, **pv_dict))

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_create_anon_user_allow_create(self):
        '''
        Calling powerview create with anon user when allow_user_create is
        true, still raises NotAuthorized.
        '''
        context = {'user': '', 'model': model}
        pv_dict = self._make_create_data_dict()
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_create', context=context,
                                **pv_dict)

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_create_normal_user_allow_create_private_resources(self):
        '''
        Calling powerview create with normal user when allow_user_create is
        true, with unauthorized resources, raises NotAuthorized.
        '''
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'], private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        a_user = factories.User()

        pv_dict = self._make_create_data_dict(resources=[r1['id'], r2['id']])
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_create', context=context,
                                **pv_dict)

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_create_normal_user_allow_create_authed_resources(self):
        '''
        Calling powerview create with normal user when allow_user_create is
        true, with authorized private resources doesn't raise NotAuthorized.
        '''
        a_user = factories.User()
        org = factories.Organization(users=[{
            'name': a_user['name'], 'capacity': 'member'}])
        dataset = factories.Dataset(owner_org=org['id'], private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        pv_dict = self._make_create_data_dict(resources=[r1['id'], r2['id']])
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_create',
                              context=context, **pv_dict))


class TestPowerViewDeleteAuth(TestBase):

    def test_powerview_delete_sysadmin(self):
        '''
        Calling powerview delete with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        pv = powerview_factories.PowerView()
        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_delete',
                                                context=context, id=pv['id']))

    def test_powerview_delete_normal_user(self):
        '''
        Calling powerview delete with normal logged in user raises
        NotAuthorized.
        '''
        a_user = factories.User()
        pv = powerview_factories.PowerView()
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_delete', context=context,
                                id=pv['id'])

    def test_powerview_delete_anon_user(self):
        '''
        Calling powerview delete with anon user raises NotAuthorized.
        '''
        context = {'user': '', 'model': model}
        pv = powerview_factories.PowerView()
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_delete', context=context,
                                id=pv['id'])

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_delete_normal_user_allow_create_owned(self):
        '''
        Calling powerview delete with normal user when allow_user_create is
        true, doesn't raise NotAuthorized for powerviews they own.
        '''
        a_user = factories.User()
        pv = powerview_factories.PowerView(user=a_user)
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_delete',
                                                context=context,
                                                id=pv['id']))

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_delete_normal_user_allow_create_unowned(self):
        '''
        Calling powerview delete with normal user when allow_user_create is
        true, raises NotAuthorized for powerviews they don't own.
        '''
        a_user = factories.User()
        pv = powerview_factories.PowerView()
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_delete', context=context,
                                id=pv['id'])

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_delete_anon_user_allow_create(self):
        '''
        Calling powerview delete with anon user when allow_user_create is
        true, still raises NotAuthorized.
        '''
        context = {'user': '', 'model': model}
        pv = powerview_factories.PowerView()
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_delete',
                                context=context,
                                id=pv['id'])


class TestPowerViewUpdateAuth(TestBase):

    def test_powerview_update_sysadmin(self):
        '''
        Calling powerview update with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        pv = powerview_factories.PowerView(private=False)
        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_update',
                                                context=context, **pv))

    def test_powerview_update_normal_user(self):
        '''
        Calling powerview update with normal logged in user raises
        NotAuthorized.
        '''
        a_user = factories.User()
        context = {'user': a_user['name'], 'model': model}
        pv = powerview_factories.PowerView(private=False)
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_update', context=context,
                                **pv)

    def test_powerview_update_anon_user(self):
        '''
        Calling powerview update with anon user raises NotAuthorized.
        '''
        context = {'user': '', 'model': model}
        pv = powerview_factories.PowerView(private=False)
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_update', context=context,
                                **pv)

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_update_normal_user_allow_create_owed(self):
        '''
        Calling powerview update with normal user when allow_user_create is
        true, doesn't raise NotAuthorized for owned powerview.
        '''
        a_user = factories.User()
        pv = powerview_factories.PowerView(user=a_user)
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_update',
                                                context=context,
                                                **pv))

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_update_normal_user_allow_create_unowed(self):
        '''
        Calling powerview update with normal user when allow_user_create is
        true, raises NotAuthorized for unowned powerview.
        '''
        a_user = factories.User()
        pv = powerview_factories.PowerView()
        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_update', context=context,
                                **pv)

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_update_anon_user_allow_create(self):
        '''
        Calling powerview update with anon user when allow_user_create is
        true, still raises NotAuthorized.
        '''
        context = {'user': '', 'model': model}
        pv = powerview_factories.PowerView(private=False)
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_update', context=context,
                                **pv)

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_update_normal_user_allow_create_add_private_resources(self):
        '''
        Calling powerview update with normal user when allow_user_create is
        true, with unauthorized private resources, raises NotAuthorized.
        '''
        a_user = factories.User()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'], private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        pv = powerview_factories.PowerView(user=a_user, private=False)
        pv['resources'] = [r1['id'], r2['id']]

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_update', context=context,
                                **pv)

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_update_normal_user_allow_create_add_authed_resources(self):
        '''
        Calling powerview update with normal user when allow_user_create is
        true, with authorized private resources doesn't raise NotAuthorized.
        '''
        a_user = factories.User()
        org = factories.Organization(users=[{'name': a_user['name'],
                                             'capacity': 'member'}])
        dataset = factories.Dataset(owner_org=org['id'], private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        pv = powerview_factories.PowerView(user=a_user, private=False)
        pv['resources'] = [r1['id'], r2['id']]

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_update',
                                                context=context, **pv))


class TestPowerViewShowAuth(TestBase):

    def test_powerview_show_sysadmin(self):
        '''
        Calling powerview show with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': model}
        powerview = powerview_factories.PowerView()
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))

    def test_powerview_show_normal_user(self):
        '''
        Calling powerview show with normal logged in user doesn't raise
        NotAuthorized for public powerview.
        '''
        a_user = factories.User()
        powerview = powerview_factories.PowerView(private='no')

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))

    def test_powerview_show_anon_user(self):
        '''
        Calling powerview show with anon user doesn't raise NotAuthorized for
        public powerview.
        '''
        powerview = powerview_factories.PowerView(private='no')

        context = {'user': '', 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))

    def test_powerview_show_normal_user_private(self):
        '''
        Calling powerview show with normal logged in user raises NotAuthorized
        for private powerview.
        '''
        a_user = factories.User()
        powerview = powerview_factories.PowerView(private='yes')

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_show',
                                context=context, id=powerview['id'])

    def test_powerview_show_anon_user_private(self):
        '''
        Calling powerview show with anon user raises NotAuthorized for private
        powerview.
        '''
        powerview = powerview_factories.PowerView(private='yes')

        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_show',
                                context=context, id=powerview['id'])

    def test_powerview_show_nonexisting_powerview(self):
        '''
        Calling powerview show with a nonexisting powerview id should raise
        NotAuthorized.
        '''
        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_show',
                                context=context, id='id-not-here')

    def test_powerview_show_private_created_by_not_sysadmin(self):
        '''
        Calling powerview show for a private powerview, that's not been
        created by a sysadmin, should allow that user to view it.'''
        a_user = factories.User()
        # making a private powerview without the usual auth, so a non-sysadmin
        # can create.
        powerview = powerview_factories.PowerView(user=a_user, private='yes',
                                                  ignore_auth=True)

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))

    def test_powerview_show_private_created_by_not_sysadmin_auth_by_syadmin(self):
        '''
        Calling powerview show for a private powerview, that's not been
        created by a sysadmin, should still allow a sysadmin to view it.'''
        a_user = factories.User()
        a_sysadmin = factories.Sysadmin()
        # making a private powerview without the usual auth, so a non-sysadmin
        # can create.
        powerview = powerview_factories.PowerView(user=a_user, private='yes',
                                                  ignore_auth=True)

        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))


class TestPowerViewAddResource(TestBase):

    def test_powerview_add_resource_sysadmin(self):
        '''
        Calling powerview add resource for a sysadmin does not raise
        NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView()

        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_add_resource',
                              context=context,
                              powerview_id=powerview['id'],
                              resource_id=r1['id']))

    def test_powerview_add_resource_normal_user(self):
        '''
        Calling powerview add resource for a normal user raises NotAuthorized.
        '''
        a_user = factories.User()
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(user=a_user)

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_add_resource',
                                context=context,
                                powerview_id=powerview['id'],
                                resource_id=r1['id'])

    def test_powerview_add_resource_anon_user(self):
        '''
        Calling powerview add resource for an anon user raises NotAuthorized.
        '''
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView()

        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_add_resource',
                                context=context,
                                powerview_id=powerview['id'],
                                resource_id=r1['id'])

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_add_resource_normal_user_allow_create(self):
        '''
        Calling powerview add resource for a normal user does not raise
        NotAuthorized for an owned powerview and resource
        '''
        a_user = factories.User()
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(user=a_user)

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_add_resource',
                              context=context,
                              powerview_id=powerview['id'],
                              resource_id=r1['id']))

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_add_resource_normal_user_allow_create_private_resource(self):
        '''
        Calling powerview add resource for a normal user raises NotAuthorized
        for an owned powerview but private unauthorized resource.
        '''
        a_user = factories.User()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'], private="true")
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(user=a_user)

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_add_resource',
                                context=context,
                                powerview_id=powerview['id'],
                                resource_id=r1['id'])

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_add_resource_normal_user_allow_create_authed_resource(self):
        '''
        Calling powerview add resource for a normal user doesn't raise
        NotAuthorized for an owned powerview and private authorized resource.
        '''
        a_user = factories.User()
        org = factories.Organization(users=[{'name': a_user['name'],
                                             'capacity': 'member'}])
        dataset = factories.Dataset(owner_org=org['id'], private="true")
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(user=a_user)

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_add_resource',
                              context=context,
                              powerview_id=powerview['id'],
                              resource_id=r1['id']))

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_add_resource_anon_user_allow_create(self):
        '''
        Calling powerview add resource for an anon user still raises
        NotAuthorized.
        '''
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView()

        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_add_resource',
                                context=context,
                                powerview_id=powerview['id'],
                                resource_id=r1['id'])


class TestPowerViewRemoveResource(TestBase):

    def test_powerview_remove_resource_sysadmin(self):
        '''
        Calling powerview remove resource for a sysadmin does not raise
        NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(resources=[r1['id']])

        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_remove_resource',
                              context=context,
                              powerview_id=powerview['id'],
                              resource_id=r1['id']))

    def test_powerview_remove_resource_normal_user(self):
        '''
        Calling powerview remove resource for a normal user raises
        NotAuthorized.
        '''
        a_user = factories.User()
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(user=a_user,
                                                  resources=[r1['id']])

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_remove_resource',
                                context=context,
                                powerview_id=powerview['id'],
                                resource_id=r1['id'])

    def test_powerview_remove_resource_anon_user(self):
        '''
        Calling powerview remove resource for an anon user raises
        NotAuthorized.
        '''
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(resources=[r1['id']])

        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_remove_resource',
                                context=context,
                                powerview_id=powerview['id'],
                                resource_id=r1['id'])

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_remove_resource_normal_user_allow_create(self):
        '''
        Calling powerview remove resource for a normal user does not raise
        NotAuthorized for an owned powerview and resource
        '''
        a_user = factories.User()
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(user=a_user,
                                                  resources=[r1['id']])

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_remove_resource',
                              context=context,
                              powerview_id=powerview['id'],
                              resource_id=r1['id']))

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_remove_resource_normal_user_allow_create_private_resource(self):
        '''
        Calling powerview remove resource for a normal user doesn't raise
        NotAuthorized for an owned powerview but private unauthorized
        resource.
        '''
        a_user = factories.User()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'], private="true")
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(user=a_user,
                                                  resources=[r1['id']])

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_remove_resource',
                              context=context,
                              powerview_id=powerview['id'],
                              resource_id=r1['id']))

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_remove_resource_normal_user_allow_create_authed_resource(self):
        '''
        Calling powerview remove resource for a normal user doesn't raise
        NotAuthorized for an owned powerview and private authorized resource.
        '''
        a_user = factories.User()
        org = factories.Organization(users=[{'name': a_user['name'],
                                             'capacity': 'member'}])
        dataset = factories.Dataset(owner_org=org['id'], private="true")
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(user=a_user,
                                                  resources=[r1['id']])

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_remove_resource',
                              context=context,
                              powerview_id=powerview['id'],
                              resource_id=r1['id']))

    @helpers.change_config('ckanext.powerview.allow_user_create', 'true')
    def test_powerview_remove_resource_anon_user_allow_create(self):
        '''
        Calling powerview remove resource for an anon user still raises
        NotAuthorized.
        '''
        dataset = factories.Dataset()
        r1 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(resources=[r1['id']])

        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_remove_resource',
                                context=context,
                                powerview_id=powerview['id'],
                                resource_id=r1['id'])


class TestPowerViewResourceListAuth(TestBase):

    def test_powerview_resource_list_sysadmin(self):
        '''
        Calling powerview resource list with a sysadmin doesn't raise
        NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        powerview = powerview_factories.PowerView(private='no')
        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_resource_list',
                              context=context, id=powerview['id']))

    def test_powerview_resource_list_normal_user(self):
        '''
        Calling powerview resource list with normal logged in user doesn't
        raise NotAuthorized.
        '''
        a_user = factories.User()
        powerview = powerview_factories.PowerView(private='no')

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_resource_list',
                              context=context,
                              id=powerview['id']))

    def test_powerview_resource_list_no_user(self):
        '''
        Calling public powerview resource list with anon user doesn't raise
        NotAuthorized.
        '''
        powerview = powerview_factories.PowerView(private='no')
        context = {'user': '', 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_resource_list',
                              context=context,
                              id=powerview['id']))

    def test_powerview_resource_list_sysadmin_private_resources(self):
        '''
        Calling powerview resource list with a sysadmin on a powerview
        containing private resources, doesn't raise errors.
        '''
        a_sysadmin = factories.Sysadmin()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'],
                                    private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(private='no',
                                                  resources=[r1['id'],
                                                             r2['id']])

        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_resource_list',
                              context=context,
                              id=powerview['id']))

    def test_powerview_resource_list_normal_user_private_resources(self):
        '''
        Calling powerview resource list with a normal user on a powerview
        containing private resources raises NotAuthorized.
        '''
        a_user = factories.User()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'],
                                    private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(private='no',
                                                  resources=[r1['id'],
                                                             r2['id']])

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_resource_list',
                                context=context,
                                id=powerview['id'])

    def test_powerview_resource_list_normal_anon_private_resources(self):
        '''
        Calling powerview resource list with an anon user on a powerview
        containing private resources raises NotAuthorized.
        '''
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'],
                                    private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        powerview = powerview_factories.PowerView(private='no',
                                                  resources=[r1['id'],
                                                             r2['id']])

        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_resource_list',
                                context=context,
                                id=powerview['id'])

    def test_powerview_resource_list_sysadmin_private_powerview(self):
        '''
        Calling powerview resource list with a sysadmin for a private
        powerview doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        powerview = powerview_factories.PowerView(private='yes')

        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_resource_list',
                              context=context,
                              id=powerview['id']))

    def test_powerview_resource_list_normal_user_private_powerview(self):
        '''
        Calling powerview resource list with a normal user on a private
        powerview raises NotAuthorized.
        '''
        a_user = factories.User()
        powerview = powerview_factories.PowerView(private='yes')

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_resource_list',
                                context=context,
                                id=powerview['id'])

    def test_powerview_resource_list_anon_user_private_powerview(self):
        '''
        Calling powerview resource list with an anon user on a private
        powerview raises NotAuthorized.
        '''
        powerview = powerview_factories.PowerView(private='yes')

        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_resource_list',
                                context=context,
                                id=powerview['id'])


class TestPowerViewListAuth(TestBase):

    def test_powerview_list_sysadmin(self):
        '''
        Calling powerview list with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_list',
                              context=context))

    def test_powerview_list_normal_user(self):
        '''
        Calling powerview list with normal logged in user doesn't raise
        NotAuthorized.
        '''
        a_user = factories.User()

        context = {'user': a_user['name'], 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_list',
                              context=context))

    def test_powerview_list_no_user(self):
        '''
        Calling powerview list with anon user doesn't raise NotAuthorized.
        '''
        context = {'user': '', 'model': model}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_list',
                              context=context))
