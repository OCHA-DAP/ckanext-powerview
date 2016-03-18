from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests import helpers, factories
from ckantoolkit import NotAuthorized

from ckanext.powerview.tests import TestBase


def _make_powerview(user, private='yes', ignore_auth=False):
    '''Make a powerview and return the resulting data_dict.'''
    data_dict = {
        'title': 'Title',
        'description': 'My short description.',
        'view_type': 'my-view-type',
        'config': '{"my":"json"}',
        'private': private
    }
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

    def test_powerview_create_no_user(self):
        '''
        Calling powerview create with no user raises NotAuthorized.
        '''
        context = {'user': None, 'model': None}
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

    def test_powerview_delete_no_user(self):
        '''
        Calling powerview delete with no user raises NotAuthorized.
        '''
        context = {'user': None, 'model': None}
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

    def test_powerview_update_no_user(self):
        '''
        Calling powerview update with no user raises NotAuthorized.
        '''
        context = {'user': None, 'model': None}
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

    def test_powerview_show_no_user(self):
        '''
        Calling powerview show with no user doesn't raise NotAuthorized for
        public powerview.
        '''
        a_sysadmin = factories.Sysadmin()
        powerview = _make_powerview(a_sysadmin, private='no')

        context = {'user': None, 'model': None}
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

    def test_powerview_show_no_user_private(self):
        '''
        Calling powerview show with no user raises NotAuthorized for private
        powerview.
        '''
        a_sysadmin = factories.Sysadmin()
        powerview = _make_powerview(a_sysadmin, private='yes')

        context = {'user': None, 'model': None}
        nosetools.assert_raises(NotAuthorized, helpers.call_auth,
                                'ckanext_powerview_show',
                                context=context, id=powerview['id'])

    def test_powerview_show_nonexisting_powerview(self):
        '''
        Calling powerview show with a nonexisting powerview id should raise
        NotAuthorized.
        '''
        context = {'user': None, 'model': None}
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
