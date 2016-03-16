from ckantoolkit.tests.helpers import reset_db

from ckanext.powerview.model import init_tables


class TestBase():

    '''Ensure powerview tables exist.'''

    @classmethod
    def setup_class(cls):
        reset_db()
        init_tables()

    def setup(self):
        reset_db()
