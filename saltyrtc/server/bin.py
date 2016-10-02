"""
The command line interface for the SaltyRTC signalling server.
"""
import asyncio
import os
import signal

import click

from . import __version__ as _version
from . import (
    server,
    util,
)


def _h(text):
    """
    For some reason, :mod:`click` does not strip new line characters
    from helps in :func:`click.option` (although it does strip them
    from helps for :func:`click.command`). So, we have to do it
    ourselves.
    """
    return text.replace('\n', '')


@click.group()
@click.pass_context
def cli(ctx):
    """
    Command Line Interface. Use --help for details.
    """
    ctx.obj = {}


@cli.command(short_help='Show version information.', help="""
Show the current version of the SaltyRTC signalling server and the
implemented protocol versions.
""")
def version():
    click.echo('Version: {}'.format(_version))
    click.echo('Protocols: {}'.format(server.Server.subprotocols))


@cli.command(short_help='Start the signalling server.', help="""
Start the SaltyRTC signalling server. A HUP signal will restart the
server and reload the SSL certificate, the SSL private key and the
private permanent key of the server.""")
@click.option('-sc', '--sslcert', type=click.Path(exists=True), help=_h("""
Path to a file that contains the SSL certificate."""))
@click.option('-sk', '--sslkey', type=click.Path(exists=True), help=_h("""
Path to a file that contains the SSL private key. Will be read from
the SSL certificate file if not present."""))
@click.option('-k', '--key', type=click.Path(exists=True), help=_h("""
Path to a or a hex-encoded private permanent key of the server (e.g.
a NaCl private key)."""))
@click.option('-h', '--host', help='Bind to a specific host.')
@click.option('-p', '--port', default=443, help='Listen on a specific port.')
@click.option('-l', '--loop', type=click.Choice(['asyncio', 'uvloop']), default='asyncio',
              help="Use a specific asyncio-compatible event loop. Defaults to 'asyncio'.")
@click.pass_context
def serve(ctx, **arguments):
    # Get arguments
    ssl_cert = arguments.get('sslcert', None)
    ssl_key = arguments.get('sslkey', None)
    key = arguments.get('key', None)
    host = arguments.get('host')
    port = arguments['port']
    loop = arguments['loop']
    safety_off = os.environ.get('SALTYRTC_SAFETY_OFF') == 'yes-and-i-know-what-im-doing'

    # Make sure the user provides cert & keys or has safety turned off
    if ssl_cert is None or key is None:
        if safety_off:
            click.echo(('It is RECOMMENDED to use SaltyRTC with both a SSL '
                       'certificate and a server permanent key'), err=True)
        else:
            click.echo(('It is REQUIRED to provide a SSL certificate and a server '
                        'permanent key unless the environment variable '
                        "'SALTYRTC_SAFETY_OFF' is set to "
                        "'yes-and-i-know-what-im-doing'"), err=True)
            ctx.exit(code=2)
            return

    # Create SSL context
    ssl_context = None
    if ssl_cert is not None:
        ssl_context = util.create_ssl_context(certfile=ssl_cert, keyfile=ssl_key)

    # Get private permanent key of the server
    if key is not None:
        key = util.load_permanent_key(key)

    # Set event loop policy
    if loop == 'uvloop':
        try:
            import uvloop
        except ImportError:
            click.echo("Cannot use event loop 'uvloop', make sure it is installed.",
                       err=True)
            ctx.exit(3)
            return
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Get event loop
    loop = asyncio.get_event_loop()

    while True:
        # Run the server
        click.echo('Starting')
        coroutine = server.serve(ssl_context, key, host=host, port=port, loop=loop)
        server_ = loop.run_until_complete(coroutine)

        # Restart server on HUP signal
        restart_signal = asyncio.Future(loop=loop)

        def _restart_signal_handler(*_):
            restart_signal.set_result(True)

        # Register restart server routine
        try:
            loop.add_signal_handler(signal.SIGHUP, _restart_signal_handler)
        except RuntimeError:
            click.echo('Cannot restart on SIGHUP, signal handler could not be added.')

        # Wait until Ctrl+C has been pressed
        click.echo('Started')
        try:
            loop.run_until_complete(restart_signal)
        except KeyboardInterrupt:
            click.echo()

        # Remove the signal handler
        loop.remove_signal_handler(signal.SIGHUP)

        # Close the server
        click.echo('Stopping')
        server_.close()
        loop.run_until_complete(server_.wait_closed())
        click.echo('Stopped')

        # Stop?
        if not restart_signal.done():
            restart_signal.cancel()
            break

    # Close loop
    loop.close()


def main():
    # TODO: Read keys from export if set (see restartable.py)
    # TODO: Add *logging* option
    # noinspection PyPackageRequirements
    import logbook.more

    # Enable asyncio debug logging
    os.environ['PYTHONASYNCIODEBUG'] = '1'

    # Enable logging
    util.enable_logging(level=logbook.TRACE, redirect_loggers={
        'asyncio': logbook.DEBUG,
        'websockets': logbook.DEBUG,
    })

    # Run 'main'
    logging_handler = logbook.more.ColorizedStderrHandler()
    with logging_handler.applicationbound():
        try:
            cli()
        except Exception as exc:
            click.echo('An error occurred:', err=True)
            click.echo(exc, err=True)
            raise