from __future__ import absolute_import

import argparse
import os

import smokesignal

from twisted.internet import reactor, ssl

from helga import settings


def run():
    """
    Run the helga process
    """
    # XXX: Delayed import so we use properly overridden settings
    from helga import comm

    smokesignal.emit('started')

    factory = comm.Factory()
    if settings.SERVER.get('SSL', False):
        reactor.connectSSL(settings.SERVER['HOST'],
                           settings.SERVER['PORT'],
                           factory,
                           ssl.ClientContextFactory())
    else:
        reactor.connectTCP(settings.SERVER['HOST'],
                           settings.SERVER['PORT'],
                           factory)
    reactor.run()


def main():
    """
    Main entry point for the helga console script
    """
    parser = argparse.ArgumentParser(description='The helga IRC bot')
    parser.add_argument('--settings', help=(
        'Custom helga settings overrides. This should be an importable python module '
        'like "foo.bar.baz" or a path to a settings file like "path/to/settings.py". '
        'This can also be set via the HELGA_SETTINGS environment variable, however '
        'this flag takes precedence.'
    ))
    args = parser.parse_args()

    settings_file = os.environ.get('HELGA_SETTINGS', '')

    if args.settings:
        settings_file = args.settings

    settings.configure(settings_file)
    run()