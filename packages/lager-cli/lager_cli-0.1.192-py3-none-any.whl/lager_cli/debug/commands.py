"""
    lager.debug.commands

    Debug an elf file
"""
import click
from ..context import get_default_gateway
from ..debug.gdb import debug
from ..gateway.commands import _status
from ..paramtypes import MemoryAddressType, HexArrayType
from ..openocd.commands import run_openocd_tunnel
from ..context import get_impl_path
from ..python.commands import run_python_internal


@click.group(name='debug')
def _debug():
    """
        Lager debug commands
    """
    pass

@_debug.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, default=None, help='MCU to query', type=click.INT)
def status(ctx, gateway, dut, mcu):
    gateway = gateway or dut
    _status(ctx, gateway, mcu)


@_debug.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected', hidden=True)
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--interpreter', '-i', required=False, default='default', help='Select a specific interpreter / user interface')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Print verbose debug info')
@click.option('--tty', required=False, help='Use TTY for input/output by the program being debugged.')
@click.option('--quiet', '--silent', '-q', is_flag=True, default=False, help='Do not print the introductory and copyright messages. These messages are also suppressed in batch mode.')
@click.option('--args', required=False, help='Arguments passed to debugger')
@click.option('--ignore-missing/--no-ignore-missing', is_flag=True, default=True, help='Ignore missing files')
@click.option('--cwd', default=None, type=click.Path(exists=True, file_okay=False, resolve_path=True), help='Set current working directory')
@click.option('--cache/--no-cache', default=True, is_flag=True, help='Use cached source if ELF file unchanged', show_default=True)
@click.option('--mcu', required=False, default=None, help='MCU to query', type=click.INT)
@click.option('--elf-only', required=False, default=False, is_flag=True, help='Only send ELF file; no source')
@click.option('--debugfile', required=False, default=None, type=click.Path(), help='Debugger command file')
@click.argument('elf_file', type=click.Path())
def gdb(ctx, gateway, dut, interpreter, verbose, tty, quiet, args, ignore_missing, cwd, cache, mcu, elf_only, debugfile, elf_file):
    """
        Debug a DUT using an ELF file
    """
    gateway = gateway or dut
    debug(ctx, gateway, interpreter, verbose, tty, quiet, args, ignore_missing, cwd, cache, mcu, elf_only, debugfile, elf_file)


@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to connect')
@click.option('--force', is_flag=True, default=False, help='Disconnect debugger before reconnecting. If not set, connect will fail if debugger is already connected. Cannot be used with --ignore-if-connected', show_default=True)
@click.option('--ignore-if-connected', is_flag=True, default=False, help='If debugger is already connected, skip connection attempt and exit with success. Cannot be used with --force', show_default=True)
def connect(ctx, dut, mcu, force, ignore_if_connected):
    if force and ignore_if_connected:
        click.secho('Cannot specify --force and --ignore-if-connected', fg='red')
        ctx.exit(1)

    if dut is None:
        dut = get_default_gateway(ctx)
    session = ctx.obj.session
    resp = session.debug_connect(dut, mcu, force, ignore_if_connected).json()
    if resp.get('start') == 'ok':
        click.secho('Connected!', fg='green')
    elif resp.get('already_running') == 'ok':
        click.secho('Debugger already connected, ignoring', fg='green')

@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to disconnect')
def disconnect(ctx, dut, mcu):
    if dut is None:
        dut = get_default_gateway(ctx)
    session = ctx.obj.session
    session.debug_disconnect(dut, mcu).json()
    click.secho('Disconnected!', fg='green')

@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to erase')
@click.argument('start_addr', required=False, type=MemoryAddressType())
@click.argument('length', required=False, type=MemoryAddressType())
def erase(ctx, dut, mcu, start_addr, length):
    if dut is None:
        dut = get_default_gateway(ctx)
    session = ctx.obj.session
    out = session.debug_erase(dut, mcu, start_addr, length).json()
    print(out['output'])
    if 'Erasing done.' in out['output']:
        click.secho('Erased!', fg='green')
    else:
        click.secho('Erasing failed', fg='red')
        ctx.exit(1)

@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to erase')
@click.argument('start_addr', type=MemoryAddressType())
@click.argument('length', type=MemoryAddressType())
def memrd(ctx, dut, mcu, start_addr, length):
    if dut is None:
        dut = get_default_gateway(ctx)
    session = ctx.obj.session
    out = session.debug_read(dut, mcu, start_addr, length).json()
    print(out['output'])


@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to erase')
@click.option('--size', required=True, type=click.Choice(['1', '2', '4']), help='Number of bytes to write')
@click.argument('start_addr', type=MemoryAddressType())
@click.argument('data')
def memwr(ctx, dut, mcu, size, start_addr, data):
    if dut is None:
        dut = get_default_gateway(ctx)

    if data.startswith('0x') or data.startswith('0X'):
        data = data[2:]
    session = ctx.obj.session
    out = session.debug_write(dut, mcu, size, start_addr, data).json()
    print(out['output'])


@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to disconnect')
@click.option(
    '--hexfile',
    type=click.Path(exists=True),
    help='Hexfile to flash.')
def flash(ctx, dut, mcu, hexfile):
    if dut is None:
        dut = get_default_gateway(ctx)
    session = ctx.obj.session
    files = [
        ('hexfile', open(hexfile, 'rb').read()),
    ]
    if mcu:
        files.append(('mcu', mcu))

    output = session.debug_flash(dut, files).json()['output']
    print(output)
    if 'Downloading file [/tmp/jlink_hexfile.hex]...' in output and 'O.K.' in output:
        click.secho('Flashed!', fg='green')
    else:
        click.secho('Flashing failed!', fg='red')
        ctx.exit(1)



@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to disconnect')
@click.option('--halt', is_flag=True, help='Halt the DUT after reset. Default: do not halt', default=False, show_default=True)
@click.option('--verbose', is_flag=True, help='Show verbose debugger output', default=False, show_default=True)
def reset(ctx, dut, mcu, halt, verbose):
    if dut is None:
        dut = get_default_gateway(ctx)
    session = ctx.obj.session

    output = session.debug_reset(dut, mcu, halt).json()['output']
    if verbose:
        print(output)

    if 'AfterResetTarget' not in output and 'Reset: Reset device' not in output:
        click.secho('Reset failed', fg='red')
        ctx.exit(1)

    if halt:
        click.secho('Device reset & halted;', fg='green')
    else:
        click.secho('Device reset; not halted;', fg='green')


RTT_BASE_PORT = 9090

@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, default=0, type=click.INT, help='MCU number')
@click.option('--host', default='localhost', help='interface for telnet to bind. '
              'Use --host \'*\' to bind to all interfaces.', show_default=True)
@click.option('--attach/--no-attach', default=False, is_flag=True, show_default=True, help='Attach to RTT without restarting MCU')
def rtt(ctx, dut, mcu, host, attach):
    if dut is None:
        dut = get_default_gateway(ctx)

    session = ctx.obj.session
    resp = session.debug_connect(dut, mcu, False, True, attach).json()
    if resp.get('start') == 'ok':
        """successful start"""
        pass
    elif resp.get('already_running') == 'ok':
        """already running"""
        pass
    else:
        raise SystemExit('Failed to start debugger')

    port = RTT_BASE_PORT + mcu
    run_openocd_tunnel(ctx, host, None, dut, True, port)


@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, default=0, type=click.INT, help='MCU number')
@click.option('--halt', is_flag=True, help='Halt the DUT after reset. Default: do not halt', default=False, show_default=True)
def gdb_reset(ctx, dut, mcu, halt):
    if dut is None:
        dut = get_default_gateway(ctx)

    session = ctx.obj.session
    resp = session.debug_connect(dut, mcu, False, True, False).json()
    if resp.get('start') == 'ok':
        """successful start"""
        pass
    elif resp.get('already_running') == 'ok':
        """already running"""
        pass
    else:
        print(resp)
        raise SystemExit('Failed to start debugger')

    run_python_internal(
        ctx,
        get_impl_path('gdb_reset.py'),
        dut,
        image='',
        env=(),
        passenv=(),
        kill=False,
        download=(),
        allow_overwrite=False,
        signum='SIGTERM',
        timeout=0,
        detach=False,
        port=(),
        org=None,
        args=(halt, ),
    )
