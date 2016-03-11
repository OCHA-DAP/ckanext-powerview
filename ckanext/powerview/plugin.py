import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.powerview.logic.auth


class PowerviewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthFunctions)

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
