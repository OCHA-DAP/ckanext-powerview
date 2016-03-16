import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.powerview.logic.auth
import ckanext.powerview.logic.validators

import logging
log = logging.getLogger(__name__)


class PowerviewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'powerview')

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            'ckanext_powerview_create': ckanext.powerview.logic.auth.create,
            'ckanext_powerview_update': ckanext.powerview.logic.auth.update,
            'ckanext_powerview_delete': ckanext.powerview.logic.auth.delete,
            'ckanext_powerview_show': ckanext.powerview.logic.auth.show,
            # 'ckanext_powerview_add_resource': ckanext.powerview.logic.auth.add_resource,
            # 'ckanext_powerview_remove_resource': ckanext.powerview.logic.auth.remove_resource,
        }

    # IActions

    def get_actions(self):
        module_root = 'ckanext.powerview.logic.action'
        logic_functions = {}
        for module_name in ['create', 'update', 'get', 'delete']:
            module_path = '%s.%s' % (module_root, module_name,)

            module = __import__(module_path)

            for part in module_path.split('.')[1:]:
                module = getattr(module, part)

            for key, value in module.__dict__.items():
                if not key.startswith('_') and \
                    (hasattr(value, '__call__') and
                        (value.__module__ == module_path)):
                    logic_functions[key] = value

        return logic_functions

    # IValidators

    def get_validators(self):
        return {
            'powerview_id_exists':
                ckanext.powerview.logic.validators.powerview_id_exists,
            'resource_ids_in_list':
                ckanext.powerview.logic.validators.resource_ids_in_list
        }
