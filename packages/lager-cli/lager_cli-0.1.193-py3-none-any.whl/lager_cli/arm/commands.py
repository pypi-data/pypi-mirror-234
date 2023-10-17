"""
    lager.arm.commands

    Arm commands
"""
import click
from ..context import get_default_gateway
from ..context import get_impl_path
from ..python.commands import run_python_internal

def run_command(ctx, dut, args):
    if dut is None:
        dut = get_default_gateway(ctx)

    run_python_internal(
        ctx,
        get_impl_path('arm.py'),
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
        args=args,
    )

@click.group(hidden=True)
def arm():
    """
        Lager arm commands
    """
    pass

@arm.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
def position(ctx, dut):
    """
    Get arm position
    """
    run_command(ctx, dut, ['position'])


@arm.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
def disable_motor(ctx, dut):
    """
    Disable motor
    """
    run_command(ctx, dut, ['disable_motor'])

@arm.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
def enable_motor(ctx, dut):
    """
    Enable motor
    """
    run_command(ctx, dut, ['enable_motor'])

@arm.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
def read_and_save_position(ctx, dut):
    """
    Read and save arm position
    """
    run_command(ctx, dut, ['read_and_save_position'])

@arm.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--x', required=False, type=click.FLOAT, help='Delta x')
@click.option('--y', required=False, type=click.FLOAT, help='Delta y')
@click.option('--z', required=False, type=click.FLOAT, help='Delta z')
@click.confirmation_option(prompt='Delta arm?')
def delta(ctx, dut, x, y, z):
    """
    Adjust position based on deltas
    """
    run_command(ctx, dut, ['delta', str(x), str(y), str(z)])


@arm.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--x', required=False, type=click.FLOAT, help='x position')
@click.option('--y', required=False, type=click.FLOAT, help='y position')
@click.option('--z', required=False, type=click.FLOAT, help='z position')
@click.confirmation_option(prompt='Move arm?')
def move(ctx, dut, x, y, z):
    """
    Move to an absolute position
    """
    run_command(ctx, dut, ['move', str(x), str(y), str(z)])

@arm.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.confirmation_option(prompt='Move arm?')
def go_home(ctx, dut):
    """
    Move the arm to its home position
    """
    run_command(ctx, dut, ['go_home'])
