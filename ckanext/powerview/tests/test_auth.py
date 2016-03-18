from nose import tools as nosetools

from ckantoolkit.tests import helpers, factories
from ckantoolkit import NotAuthorized

from ckanext.powerview.tests import TestBase


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
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context))

    def test_powerview_show_normal_user(self):
        '''
        Calling powerview show with normal logged in user doesn't raise
        NotAuthorized.
        '''
        a_user = factories.User()
        context = {'user': a_user['name'], 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context))

    def test_powerview_show_no_user(self):
        '''
        Calling powerview show with no user doesn't raise NotAuthorized.
        '''
        context = {'user': None, 'model': None}
        nosetools.assert_true(helpers.call_auth('ckanext_powerview_show',
                                                context=context))
