import sys
import logging
import traceback
from .FlaskMain import create_app, shutdown_application


def main(args):
    if 'webserver' in str(args).lower():
        create_app()

    if 'shutdown' in str(args).lower():
        # Shutdown the application
        shutdown_application()


if __name__ == "__main__":
    main(sys.argv[1:])