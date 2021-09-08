# -*- coding: utf-8 -*-

import argparse
import logging
import os

from datetime import datetime
from functools import partial

import argparse_logging
from croniter import croniter
from supervisor.childutils import listener, getRPCInterface


def cli():
    """Create ArgumentParser for the CLI."""
    parser = argparse.ArgumentParser(description="superestart")

    # what to act on
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument(
        "--group",
        type=str,
        dest="group",
        help="group name"
    )
    target.add_argument(
        "--program",
        type=str,
        dest="program",
        help="program name"
    )

    # ...and everything else.
    parser.add_argument(
        "--action",
        type=str,
        choices=['restart', 'start', 'stop'],
        default='restart',
        dest='action',
        help="the action to take on the program or group"
    )
    parser.add_argument(
        "--crontab",
        type=str,
        dest="crontab",
        required=True,
        help="crontab like string"
    )

    # logging customization, thanks!
    argparse_logging.add_logging_arguments(parser)
    return parser


def main():
    args = cli().parse_args()

    server = getRPCInterface(os.environ)

    time_iter = croniter(args.crontab, datetime.now())
    next_execute_time = time_iter.get_next(datetime)
    logging.info(f"next execution due at {next_execute_time}")

    # ugly, but YOLO.  nicer if there were some action handler that
    # stored both the name *and* the argument that were passed, but so
    # it goes.
    if args.group:
        target = args.group
        do_stop = partial(server.supervisor.stopProcessGroup, args.group)
        do_start = partial(server.supervisor.startProcessGroup, args.group)
    elif args.program:
        target = args.program
        do_stop = partial(server.supervisor.stopProcess, args.program)
        do_start = partial(server.supervisor.startProcess, args.program)

    while True:
        try:
            headers, _ = listener.wait()
            if "TICK" in headers["eventname"]:
                if datetime.now() >= next_execute_time:
                    if args.action in ['stop', 'restart']:
                        logging.info(f'stopping {target}')
                        do_stop()
                    if args.action in ['start', 'restart']:
                        logging.info(f'starting {target}')
                        do_start()

                    next_execute_time = time_iter.get_next(datetime)
                    logging.info(f"next execution due at {next_execute_time}")
            listener.ok()
        except Exception:
            listener.fail()
            raise


if __name__ == "__main__":
    main()
