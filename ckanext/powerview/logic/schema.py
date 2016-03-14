from ckan.plugins import toolkit

not_missing = toolkit.get_validator('not_missing')
ignore_missing = toolkit.get_validator('ignore_missing')
package_exists = toolkit.get_validator('package_id_or_name_exists')
resource_id_exists = toolkit.get_validator('resource_id_exists')
user_exists = toolkit.get_validator('user_id_or_name_exists')
organization_exists = toolkit.get_validator('group_id_or_name_exists')
boolean_validator = toolkit.get_validator('boolean_validator')
empty = toolkit.get_validator('empty')
not_empty = toolkit.get_validator('not_empty')
convert_to_json_if_string = toolkit.get_converter('convert_to_json_if_string')


def powerview_base_schema():
    schema = {
        'title': [not_empty, unicode],
        'description': [ignore_missing, unicode],
        'view_type': [not_empty, unicode],
        'config': [ignore_missing, convert_to_json_if_string],
        'private': [ignore_missing, boolean_validator]
    }
    return schema


def powerview_create_schema():
    schema = powerview_base_schema()
    schema.update({
        'id': [empty]
    })
    return schema
