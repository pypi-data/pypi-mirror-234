import argparse
import os

from bec_server.service_handler import ServiceHandler


def main():
    """
    Launch the BEC server in a tmux session. All services are launched in separate panes.
    """
    parser = argparse.ArgumentParser(description="Utility tool managing the BEC server")
    command = parser.add_subparsers(dest="command")
    start = command.add_parser("start", help="Start the BEC server")
    start.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to the BEC service config file",
    )
    command.add_parser("stop", help="Stop the BEC server")
    restart = command.add_parser("restart", help="Restart the BEC server")
    restart.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to the BEC service config file",
    )
    command.add_parser("status", help="Show the status of the BEC server")

    args = parser.parse_args()

    if "config" in args:
        config = args.config
    else:
        config = None

    service_handler = ServiceHandler(
        bec_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        config_path=config,
    )
    if args.command == "start":
        service_handler.start()
    elif args.command == "stop":
        service_handler.stop()
    elif args.command == "restart":
        service_handler.restart()
