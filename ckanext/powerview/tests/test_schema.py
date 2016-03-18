from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin, Resource

from ckantoolkit import ValidationError

from ckanext.powerview.tests import TestBase


def _make_powerview(user):
    '''Make a powerview and return the resulting data_dict.'''
    data_dict = {
        'title': 'Title',
        'description': 'My short description.',
        'view_type': 'my-view-type',
        'config': '{"my":"json"}',
        'private': 'yes'
    }

    return toolkit.get_action('powerview_create')(
        context={'user': user['name']},
        data_dict=data_dict
    )


class TestCreatePowerView(TestBase):

    '''Test schema validation for powerview_create.'''

    def _make_create_data_dict(self):
        data_dict = {
            'title': 'Title',
            'description': 'My short description.',
            'view_type': 'my-view-type',
            'config': '{"my":"json"}',
            'private': 'yes'
        }
        return data_dict

    def test_powerview_create_title(self):
        '''Providing title doesn't raise ValidationError.'''
        sysadmin = Sysadmin()

        data_dict = self._make_create_data_dict()
        toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=data_dict
        )

    def test_powerview_create_title_missing(self):
        '''Missing title raises ValidationError.'''
        sysadmin = Sysadmin()

        data_dict = self._make_create_data_dict()
        # remove title key
        del data_dict['title']
        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_create')(
                context={'user': sysadmin['name']},
                data_dict=data_dict
            )
        error_dict = cm.exception.error_dict['title']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_create_description_optional(self):
        '''Missing description doesn't raise ValidationError.'''
        sysadmin = Sysadmin()

        data_dict = self._make_create_data_dict()
        # remove description key
        del data_dict['description']
        toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=data_dict
        )

    def test_powerview_create_view_type_missing(self):
        '''Missing view_type raises ValidationError.'''
        sysadmin = Sysadmin()

        data_dict = self._make_create_data_dict()
        # remove title key
        del data_dict['view_type']
        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_create')(
                context={'user': sysadmin['name']},
                data_dict=data_dict
            )
        error_dict = cm.exception.error_dict['view_type']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_create_config(self):
        '''Missing config doesn't raise ValidationError.'''
        sysadmin = Sysadmin()

        data_dict = self._make_create_data_dict()
        # remove config key
        del data_dict['config']
        toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=data_dict
        )

    def test_powerview_create_config_must_be_json(self):
        '''If present, config must be a json string.'''
        sysadmin = Sysadmin()

        data_dict = self._make_create_data_dict()
        # replace config with non-json string
        data_dict['config'] = "I'm not json."
        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_create')(
                context={'user': sysadmin['name']},
                data_dict=data_dict
            )
        error_dict = cm.exception.error_dict['config']
        nosetools.assert_true("Could not parse as valid JSON"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_create_private_missing(self):
        '''Missing private doesn't raise ValidationError.'''
        sysadmin = Sysadmin()
        data_dict = self._make_create_data_dict()
        # remove private key
        del data_dict['private']
        toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=data_dict
        )

    def test_powerview_create_id_must_be_empty(self):
        '''id must be missing if creating a powerview.'''
        sysadmin = Sysadmin()
        data_dict = self._make_create_data_dict()
        # add an id key
        data_dict['id'] = 'my-id'
        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_create')(
                context={'user': sysadmin['name']},
                data_dict=data_dict
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("The input field id was not expected."
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_create_resource_list_must_be_list(self):
        '''resources must be a list'''
        sysadmin = Sysadmin()
        data_dict = self._make_create_data_dict()
        # add invalid resource list
        data_dict['resources'] = "Isn't a list"
        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_create')(
                context={'user': sysadmin['name']},
                data_dict=data_dict
            )
        error_dict = cm.exception.error_dict['resources']
        nosetools.assert_true("Not a list"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_create_resources_must_be_strings(self):
        '''Items in resources list must be strings'''
        sysadmin = Sysadmin()
        data_dict = self._make_create_data_dict()
        # add invalid resource list
        data_dict['resources'] = [1, 'asfd']
        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_create')(
                context={'user': sysadmin['name']},
                data_dict=data_dict
            )
        error_dict = cm.exception.error_dict['resources']
        nosetools.assert_true("Not a string: 1"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_create_resources_ids_must_exist(self):
        '''Items in resources list must be resource ids that exist.'''
        sysadmin = Sysadmin()
        data_dict = self._make_create_data_dict()
        # add invalid resource list
        data_dict['resources'] = ['my-nonexisting-id', 'resource-not-here']
        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_create')(
                context={'user': sysadmin['name']},
                data_dict=data_dict
            )
        error_dict = cm.exception.error_dict['resources']
        nosetools.assert_true("Not found: Resource"
                              in error_dict,
                              "Expected string not in exception message.")


class TestUpdatePowerView(TestBase):

    '''Test schema validation for powerview update.'''

    def _make_powerview(self, user):
        '''Make a powerview and return the resulting data_dict.'''
        data_dict = {
            'title': 'Title',
            'description': 'My short description.',
            'view_type': 'my-view-type',
            'config': '{"my":"json"}',
            'private': 'yes'
        }

        return toolkit.get_action('powerview_create')(
            context={'user': user['name']},
            data_dict=data_dict
        )

    def test_powerview_update_valid_dict(self):
        '''Updating with valid data_dict passes schema validation with no
        errors raised.'''
        sysadmin = Sysadmin()

        powerview_dict_create = self._make_powerview(sysadmin)

        # update with the same data_dict as returned by create
        toolkit.get_action('powerview_update')(
            context={'user': sysadmin['name']},
            data_dict=powerview_dict_create.copy()
        )

    def test_powerview_update_no_id(self):
        '''Updating with a missing powerview id raises error.'''

        sysadmin = Sysadmin()

        powerview_dict = self._make_powerview(sysadmin)
        del powerview_dict['id']

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_update')(
                context={'user': sysadmin['name']},
                data_dict=powerview_dict
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_update_nonexisting_id(self):
        '''Updating with a non-existing powerview id raises error.'''

        sysadmin = Sysadmin()

        powerview_dict = self._make_powerview(sysadmin)
        powerview_dict['id'] = 'non-existing-id'

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_update')(
                context={'user': sysadmin['name']},
                data_dict=powerview_dict
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Not found: PowerView"
                              in error_dict,
                              "Expected string not in exception message.")


class TestShowPowerView(TestBase):

    '''Test schema validation for powerview show.'''

    def test_powerview_show_valid_dict(self):
        '''Calling powerview show with valid id passes schema validation with
        no errors raised.'''
        sysadmin = Sysadmin()

        powerview_dict = _make_powerview(sysadmin)

        toolkit.get_action('powerview_show')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict['id']}
        )

    def test_powerview_show_no_id(self):
        '''Calling powerview show with a missing id raises error.'''

        sysadmin = Sysadmin()

        _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_show')(
                context={'user': sysadmin['name']},
                data_dict={}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_show_nonexisting_id(self):
        '''Calling powerview show with a non-existing id raises error.'''

        sysadmin = Sysadmin()

        _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_show')(
                context={'user': sysadmin['name']},
                data_dict={'id': 'non-existin-id'}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Not found: PowerView"
                              in error_dict,
                              "Expected string not in exception message.")


class TestPowerViewResourceList(TestBase):

    '''Test schema validation for powerview resourse list.'''

    def test_powerview_resource_list_valid_dict(self):
        '''Calling powerview resource list with valid id passes schema
        validation with no errors raised.'''
        sysadmin = Sysadmin()

        powerview_dict = _make_powerview(sysadmin)

        toolkit.get_action('powerview_resource_list')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict['id']}
        )

    def test_powerview_resource_list_no_id(self):
        '''Calling powerview resource list with a missing id raises error.'''
        sysadmin = Sysadmin()

        _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_resource_list')(
                context={'user': sysadmin['name']},
                data_dict={}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_resource_list_nonexisting_id(self):
        '''Calling powerview resource list with a non-existing id raises
        error.'''
        sysadmin = Sysadmin()

        _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_resource_list')(
                context={'user': sysadmin['name']},
                data_dict={'id': 'non-existin-id'}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Not found: PowerView"
                              in error_dict,
                              "Expected string not in exception message.")


class TestDeletePowerView(TestBase):

    '''Test schema validation for powerview delete.'''

    def test_powerview_delete_valid_id(self):
        '''powerview delete passes schema validation with no errors raised.'''
        sysadmin = Sysadmin()

        powerview_dict = _make_powerview(sysadmin)

        toolkit.get_action('powerview_delete')(
            context={'user': sysadmin['name']},
            data_dict={'id': powerview_dict['id']}
        )

    def test_powerview_delete_no_id(self):
        '''Calling powerview delete with a missing id raises error.'''

        sysadmin = Sysadmin()

        _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_delete')(
                context={'user': sysadmin['name']},
                data_dict={}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_delete_nonexisting_id(self):
        '''Calling powerview delete with a non-existing id raises error.'''

        sysadmin = Sysadmin()

        _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_delete')(
                context={'user': sysadmin['name']},
                data_dict={'id': 'non-existin-id'}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Not found: PowerView"
                              in error_dict,
                              "Expected string not in exception message.")


class TestPowerviewResourceAdd(TestBase):

    '''Test schema validation for powerview_add_resource action.'''

    def test_powerview_add_resource_no_powerview_id(self):
        '''Calling powerview_add_resource with no powerview id raises
        ValidationError.'''
        sysadmin = Sysadmin()
        res = Resource()

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_add_resource')(
                context={'user': sysadmin['name']},
                data_dict={'resource_id': res['id']}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_add_resource_no_resource_id(self):
        '''Calling powerview_add_resource with no resource id raises
        ValidationError.'''
        sysadmin = Sysadmin()
        powerview = _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_add_resource')(
                context={'user': sysadmin['name']},
                data_dict={'id': powerview['id']}
            )
        error_dict = cm.exception.error_dict['resource_id']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_add_resource_nonexisting_powerview_id(self):
        '''Calling powerview_add_resource with a nonexisting powerview id
        raises ValidationError.'''
        sysadmin = Sysadmin()
        res = Resource()

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_add_resource')(
                context={'user': sysadmin['name']},
                data_dict={'resource_id': res['id'], 'id': 'non-existing-id'}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Not found: PowerView"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_add_resource_nonexisting_resource_id(self):
        '''Calling powerview_add_resource with nonexisting resource id raises
        ValidationError.'''
        sysadmin = Sysadmin()
        powerview = _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_add_resource')(
                context={'user': sysadmin['name']},
                data_dict={'id': powerview['id'],
                           'resource_id': 'non-existing-id'}
            )
        error_dict = cm.exception.error_dict['resource_id']
        nosetools.assert_true("Not found: Resource"
                              in error_dict,
                              "Expected string not in exception message.")


class TestPowerviewResourceRemove(TestBase):

    '''Test schema validation for powerview_remove_resource action.'''

    def test_powerview_remove_resource_no_powerview_id(self):
        '''Calling powerview_remove_resource with no powerview id raises
        ValidationError.'''
        sysadmin = Sysadmin()
        res = Resource()

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_remove_resource')(
                context={'user': sysadmin['name']},
                data_dict={'resource_id': res['id']}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_remove_resource_no_resource_id(self):
        '''Calling powerview_remove_resource with no resource id raises
        ValidationError.'''
        sysadmin = Sysadmin()
        powerview = _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_remove_resource')(
                context={'user': sysadmin['name']},
                data_dict={'id': powerview['id']}
            )
        error_dict = cm.exception.error_dict['resource_id']
        nosetools.assert_true("Missing value"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_remove_resource_nonexisting_powerview_id(self):
        '''Calling powerview_remove_resource with a nonexisting powerview id
        raises ValidationError.'''
        sysadmin = Sysadmin()
        res = Resource()

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_remove_resource')(
                context={'user': sysadmin['name']},
                data_dict={'resource_id': res['id'], 'id': 'non-existing-id'}
            )
        error_dict = cm.exception.error_dict['id']
        nosetools.assert_true("Not found: PowerView"
                              in error_dict,
                              "Expected string not in exception message.")

    def test_powerview_remove_resource_nonexisting_resource_id(self):
        '''Calling powerview_remove_resource with nonexisting resource id raises
        ValidationError.'''
        sysadmin = Sysadmin()
        powerview = _make_powerview(sysadmin)

        with nosetools.assert_raises(ValidationError) as cm:
            toolkit.get_action('powerview_remove_resource')(
                context={'user': sysadmin['name']},
                data_dict={'id': powerview['id'],
                           'resource_id': 'non-existing-id'}
            )
        error_dict = cm.exception.error_dict['resource_id']
        nosetools.assert_true("Not found: Resource"
                              in error_dict,
                              "Expected string not in exception message.")
