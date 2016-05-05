from ckan.plugins import toolkit

ignore_missing = toolkit.get_validator('ignore_missing')
resource_id_exists = toolkit.get_validator('resource_id_exists')
organization_exists = toolkit.get_validator('group_id_or_name_exists')
boolean_validator = toolkit.get_validator('boolean_validator')
empty = toolkit.get_validator('empty')
not_empty = toolkit.get_validator('not_empty')
convert_to_json_if_string = toolkit.get_converter('convert_to_json_if_string')
powerview_id_exists = toolkit.get_validator('powerview_id_exists')
resource_ids_in_list = toolkit.get_validator('resource_ids_in_list')
resource_id_exists = toolkit.get_validator('resource_id_exists')
natural_number_validator = toolkit.get_validator('natural_number_validator')


def powerview_base_schema():
    schema = {
        'title': [not_empty, unicode],
        'description': [ignore_missing, unicode],
        'view_type': [not_empty, unicode],
        'config': [ignore_missing, convert_to_json_if_string],
        'private': [ignore_missing, boolean_validator],
        'resources': [ignore_missing, resource_ids_in_list]
    }
    return schema


def powerview_create_schema():
    schema = powerview_base_schema()
    schema.update({
        'id': [empty]
    })
    return schema


def powerview_update_schema():
    schema = powerview_base_schema()
    schema.update({
        'id': [not_empty, unicode, powerview_id_exists]
    })
    return schema


def powerview_show_schema():
    schema = {
        'id': [not_empty, unicode, powerview_id_exists]
    }
    return schema


def powerview_delete_schema():
    schema = {
        'id': [not_empty, unicode, powerview_id_exists]
    }
    return schema


def powerview_resource_association_create_schema():
    schema = {
        'id': [not_empty, unicode, powerview_id_exists],
        'resource_id': [not_empty, unicode, resource_id_exists]
    }
    return schema


def powerview_resource_association_delete_schema():
    schema = {
        'id': [not_empty, unicode, powerview_id_exists],
        'resource_id': [not_empty, unicode, resource_id_exists]
    }
    return schema


def powerview_resource_list():
    schema = {
        'id': [not_empty, unicode, powerview_id_exists],
    }
    return schema


def default_pagination_schema():
    schema = {
        'limit': [ignore_missing, natural_number_validator],
        'offset': [ignore_missing, natural_number_validator]
    }
    return schema
