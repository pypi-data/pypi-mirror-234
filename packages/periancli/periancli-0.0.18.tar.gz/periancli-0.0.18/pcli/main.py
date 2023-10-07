
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import MyAppError
from .controllers.base import Base
from .controllers.flavor import Flavor
from .controllers.job import Job
from .controllers.config import Config
from .ext.db import extend_db


# configuration defaults
CONFIG = init_defaults('perian')
CONFIG['perian']['db_file'] = '~/.perian/db.json'


class PerianCli(App):
    """Perian Platform CLI primary application."""

    class Meta:
        label = 'pcli'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        close_on_exit = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # template dirs
        template_dir = './templates'

        # register handlers
        handlers = [
            Base,
            Flavor,
            Job,
            Config
        ]

        # register hooks
        hooks = [
            ('post_setup', extend_db),
        ]


class MyAppTest(TestApp,PerianCli):
    """A sub-class of MyApp that is better suited for testing."""

    class Meta:
        label = 'perian'


def main():
    with PerianCli() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except MyAppError as e:
            print('MyAppError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
