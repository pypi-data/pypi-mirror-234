"""Main Module of CLI"""
#!/usr/bin/env python3
import argparse
import logging
import os
import platform
import sys

import flywheel

from . import monkey, util
from .commands import add_commands
from .config import Config, ConfigError
from .fwlogging import ColorLogging

# Configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(ColorLogging())
log.addHandler(console_handler)


def main(args=None):
    """Main function"""
    # Handle fs weirdness
    monkey.patch_fs()

    # Disable terminal colors if NO_COLOR is set
    if os.environ.get("NO_COLOR"):
        import crayons

        crayons.disable()

    # Global exception handler for KeyboardInterrupt
    sys.excepthook = ctrlc_excepthook

    # Create base parser and subparsers
    parser = argparse.ArgumentParser(
        prog="fw", description="Flywheel command-line interface"
    )

    # Add commands from commands module
    add_commands(parser)

    # Read system argument passed and print warnings/messages
    sub_command = sys.argv
    # load dict of deprecated arguments
    depr_command = Config.deprecated_parsers()
    # compare deprecated arguments with parsed arguments
    isx = list(set(list(depr_command.keys())).intersection(sub_command))
    # print warning if deprecated argument parsed
    if len(isx) > 0:
        for cmd in isx:
            log.warning(depr_command[cmd])

    # Parse arguments
    args = parser.parse_args(args)

    # Read duplicate option from config file. FLYW-10930
    Config.load_duplicates(args)

    # Additional configuration
    try:
        config_fn = getattr(args, "config", None)
        if callable(config_fn):
            config_fn(args)
    except ConfigError as err:
        util.perror(err)
        sys.exit(1)

    log.debug(f"CLI Version: {util.get_cli_version()}")
    log.debug(f"CLI Args: {sys.argv}")
    log.debug(f"Platform: {platform.platform()}")
    log.debug(f"System Encoding: {sys.stdout.encoding}")
    log.debug(f"Python Version: {sys.version}")

    func = getattr(args, "func", None)
    if func is not None:
        # Invoke command
        try:
            rc = args.func(args)
            if rc is None:
                rc = 0
        except flywheel.ApiException as exc:
            log.debug("Uncaught ApiException", exc_info=True)
            if exc.status == 401:
                util.perror(f'You are not authorized: {exc.detail or "unknown reason"}')
                util.perror("Maybe you need to refresh your API key and login again?")
            else:
                util.perror(f"Request failed: {exc.detail or exc}")
            rc = 1
        except Exception as exc:
            log.debug("Uncaught Exception", exc_info=True)
            util.perror(f"Error: {exc}")
            rc = 1
    else:
        parser.print_help()
        rc = 1

    sys.exit(rc)


def ctrlc_excepthook(exctype, value, traceback):
    """Exit CLI with Ctrl+C"""
    if exctype == KeyboardInterrupt:
        util.perror("\nUser cancelled execution (Ctrl+C)")
        logging.getLogger().setLevel(100)  # Supress any further log output
        os._exit(1)
    else:
        sys.__excepthook__(exctype, value, traceback)


if __name__ == "__main__":
    main()
