import factory

from ckantoolkit.tests import helpers

from ckanext.powerview.model import PowerView


def _get_action_user_name(kwargs):
    '''Return the name of the user in kwargs, defaulting to the site user

    It can be overriden by explictly setting {'user': None} in the keyword
    arguments. In that case, this method will return None.
    '''

    if 'user' in kwargs:
        user = kwargs['user']
    else:
        user = helpers.call_action('get_site_user')

    if user is None:
        user_name = None
    else:
        user_name = user['name']

    return user_name


class PowerView(factory.Factory):
    '''A factory class for creating ckanext powerviews.'''

    FACTORY_FOR = PowerView

    # These are the default params that will be used to create new powerviews.
    title = 'Test Powerview'
    description = 'My test powerview description.'
    view_type = 'my-view-type'
    config = '{"my": "json"}'
    private = 'yes'

    # # Generate a different group name param for each user that gets created.
    # name = factory.Sequence(lambda n: 'test_dataset_{n}'.format(n=n))

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': _get_action_user_name(kwargs)}

        dataset_dict = helpers.call_action('powerview_create',
                                           context=context,
                                           **kwargs)
        return dataset_dict
