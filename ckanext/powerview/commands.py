import logging

from ckan.lib.cli import CkanCommand


class Powerview(CkanCommand):
    '''
    paster powerview init
        - Creates the database tables powerview needs to run.
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    min_args = 0
    max_args = 2

    def command(self):
        '''
        Parse command line arguments and call appropriate method.
        '''

        cmd = self.args[0]
        self._load_config()

        # Initialise logger after the config is loaded, so it is not disabled.
        self.log = logging.getLogger(__name__)

        if cmd == 'init':
            from ckanext.powerview.model import init_tables
            init_tables()
