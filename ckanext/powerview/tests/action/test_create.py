from nose import tools as nosetools

import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckantoolkit.tests.factories import Sysadmin
from ckantoolkit.tests.helpers import FunctionalTestBase


class TestCreatePowerView(FunctionalTestBase):

    def _make_create_data_dict(self):
        data_dict = {
            'title': 'Title',
            'description': 'My short description.',
            'view_type': 'my-view-type',
            'config': '{"my":"json"}',
            'private': 'yes'
        }
        return data_dict

    def test_powerview_create(self):
        sysadmin = Sysadmin()

        toolkit.get_action('powerview_create')(
            context={'user': sysadmin['name']},
            data_dict=self._make_create_data_dict()
        )
