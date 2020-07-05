"""Standalone Demodulator"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from . import rp, firewall, defs, config


def subparser(subparsers):
    p = subparsers.add_parser('standalone',
                              description="Standalone DVB-S2 receiver manager",
                              help='Manage the standalone DVB-S2 receiver',
                              formatter_class=ArgumentDefaultsHelpFormatter)
    p.add_argument('-i', '--interface',
                    default=None,
                    help='Network interface connected to the standalone \
                    demodulator')
    p.add_argument('-y', '--yes', default=False, action='store_true',
                   help="Default to answering Yes to configuration prompts")
    p.set_defaults(func=print_help)

    subsubparsers = p.add_subparsers(title='subcommands',
                                     help='Target sub-command')
    p1 = subsubparsers.add_parser('config', aliases=['cfg'],
                                  description='Initial configurations',
                                  help='Configure the host to receive data \
                                  from the standalone demodulator')
    p1.set_defaults(func=cfg_standalone)

    return p


def cfg_standalone(args):
    """Configurations for standalone DVB demodulator
    """
    # User info
    user_info = config.read_cfg_file(args.cfg, args.cfg_dir)

    if 'netdev' not in user_info['setup']:
        assert(args.interface is not None), \
            ("Please specify the network interface through option "
             "\"-i/--interface\"")

    interface = args.interface if (args.interface is not None) else \
                user_info['setup']['netdev']

    rp.set_filters([interface], prompt=(not args.yes))
    firewall.configure([interface], defs.src_ports, igmp=True,
                       prompt=(not args.yes))


def print_help(args):
    """Re-create argparse's help menu for the standalone command"""
    parser     = ArgumentParser()
    subparsers = parser.add_subparsers(title='', help='')
    parser     = subparser(subparsers)
    print(parser.format_help())

