from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit
import ckan.model as model

from ckantoolkit.tests import helpers, factories
from ckantoolkit import NotAuthorized

from ckanext.powerview.tests import TestBase


def _make_powerview(user, private='yes', ignore_auth=False, resources=None):
    '''Make a powerview and return the resulting data_dict.'''
    data_dict = {
        'title': 'Title',
        'description': 'My short description.',
        'view_type': 'my-view-type',
        'config': '{"my":"json"}',
        'private': private
    }
    if resources:
        data_dict['resources'] = resources
    context = {
        'user': user['name'],
        'ignore_auth': ignore_auth
    }

    return toolkit.get_action('powerview_create')(
        context=context,
        data_dict=data_dict
    )


class TestPowerViewCreateAuth(TestBase):

    def test_powerview_create_sysadmin(self):
        '''
        Calling powerview create with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_create',
                                                context=context))

    def test_powerview_create_normal_user(self):
        '''
        Calling powerview create with normal logged in user raises
        NotAuthorized.
        '''
        a_user = factories.User()
        context = {'user': a_user['name'], 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_create', context=context)

    def test_powerview_create_anon_user(self):
        '''
        Calling powerview create with anon user raises NotAuthorized.
        '''
        context = {'user': '', 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_create', context=context)


class TestPowerViewDeleteAuth(TestBase):

    def test_powerview_delete_sysadmin(self):
        '''
        Calling powerview delete with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_delete',
                                                context=context))

    def test_powerview_delete_normal_user(self):
        '''
        Calling powerview delete with normal logged in user raises
        NotAuthorized.
        '''
        a_user = factories.User()
        context = {'user': a_user['name'], 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_delete', context=context)

    def test_powerview_delete_anon_user(self):
        '''
        Calling powerview delete with anon user raises NotAuthorized.
        '''
        context = {'user': '', 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_delete', context=context)


class TestPowerViewUpdateAuth(TestBase):

    def test_powerview_update_sysadmin(self):
        '''
        Calling powerview update with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_update',
                                                context=context))

    def test_powerview_update_normal_user(self):
        '''
        Calling powerview update with normal logged in user raises
        NotAuthorized.
        '''
        a_user = factories.User()
        context = {'user': a_user['name'], 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_update', context=context)

    def test_powerview_update_anon_user(self):
        '''
        Calling powerview update with anon user raises NotAuthorized.
        '''
        context = {'user': '', 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_update', context=context)


class TestPowerViewShowAuth(TestBase):

    def test_powerview_show_sysadmin(self):
        '''
        Calling powerview show with a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        powerview = _make_powerview(a_sysadmin)
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                data_dict=powerview))

    def test_powerview_show_normal_user(self):
        '''
        Calling powerview show with normal logged in user doesn't raise
        NotAuthorized for public powerview.
        '''
        a_user = factories.User()
        a_sysadmin = factories.Sysadmin()
        powerview = _make_powerview(a_sysadmin, private='no')

        context = {'user': a_user['name'], 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))

    def test_powerview_show_anon_user(self):
        '''
        Calling powerview show with anon user doesn't raise NotAuthorized for
        public powerview.
        '''
        a_sysadmin = factories.Sysadmin()
        powerview = _make_powerview(a_sysadmin, private='no')

        context = {'user': '', 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))

    def test_powerview_show_normal_user_private(self):
        '''
        Calling powerview show with normal logged in user raises NotAuthorized
        for private powerview.
        '''
        a_user = factories.User()
        a_sysadmin = factories.Sysadmin()
        powerview = _make_powerview(a_sysadmin, private='yes')

        context = {'user': a_user['name'], 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_show',
                                context=context, id=powerview['id'])

    def test_powerview_show_anon_user_private(self):
        '''
        Calling powerview show with anon user raises NotAuthorized for private
        powerview.
        '''
        a_sysadmin = factories.Sysadmin()
        powerview = _make_powerview(a_sysadmin, private='yes')

        context = {'user': '', 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_show',
                                context=context, id=powerview['id'])

    def test_powerview_show_nonexisting_powerview(self):
        '''
        Calling powerview show with a nonexisting powerview id should raise
        NotAuthorized.
        '''
        context = {'user': '', 'model': None}
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
        powerview = _make_powerview(a_user, private='yes', ignore_auth=True)

        context = {'user': a_user['name'], 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))

    def test_powerview_show_private_created_by_not_sysadmin_auth_by_syadmin(self):
        '''
        Calling powerview show for a private powerview, that's not been
        created by a sysadmin, should still allow a sysadnin to view it.'''
        a_user = factories.User()
        a_sysadmin = factories.Sysadmin()
        # making a private powerview without the usual auth, so a non-sysadmin
        # can create.
        powerview = _make_powerview(a_user, private='yes', ignore_auth=True)

        context = {'user': a_sysadmin['name'], 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context,
                                                id=powerview['id']))


class TestPowerViewResourceListAuth(TestBase):

    def test_powerview_resource_list_sysadmin(self):
        '''
        Calling powerview resource list with a sysadmin doesn't raise
        NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_resource_list',
                              context=context))

    def test_powerview_resource_list_normal_user(self):
        '''
        Calling powerview resource list with normal logged in user doesn't
        raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        a_user = factories.User()
        powerview = _make_powerview(a_sysadmin, private='no')

        context = {'user': a_user['name'], 'model': None}
        nosetools.assert_true(
            helpers.call_auth('ckanext_powerview_resource_list',
                              context=context,
                              id=powerview['id']))

    def test_powerview_resource_list_no_user(self):
        '''
        Calling powerview resource list with anon user doesn't raise
        NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        powerview = _make_powerview(a_sysadmin, private='no')
        context = {'user': '', 'model': None}
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

        powerview = _make_powerview(a_sysadmin, private='no',
                                    resources=[r1['id'], r2['id']])

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
        a_sysadmin = factories.Sysadmin()
        a_user = factories.User()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'],
                                    private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        powerview = _make_powerview(a_sysadmin, private='no',
                                    resources=[r1['id'], r2['id']])

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
        a_sysadmin = factories.Sysadmin()
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'],
                                    private="true")
        r1 = factories.Resource(package_id=dataset['id'])
        r2 = factories.Resource(package_id=dataset['id'])

        powerview = _make_powerview(a_sysadmin, private='no',
                                    resources=[r1['id'], r2['id']])

        context = {'user': '', 'model': model}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_resource_list',
                                context=context,
                                id=powerview['id'])
