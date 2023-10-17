import argparse
import pathlib
import os

def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk-root', type=pathlib.Path, default=None,
                        help='Path to the Sound Designer SDK root folder (or set "SD_SDK_ROOT" in your environment)')
    parser.add_argument('--noahlink-driver-path', type=pathlib.Path, default=None,
                        help='Path to the NOAHLink Wireless drivers (when using NOAHLink wireless)')
    parser.add_argument('--programmer', choices=['RSL10', 'NOAHLink'],
                        default='RSL10',
                        help=f'The type of wireless programmer to use')
    parser.add_argument('--com-port', default='COM3',
                        help='The COM port to use when using the RSL10 dongle')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Log additional debug information to app_debug.log')
    parser.add_argument('--delete-bonds', action='store_true', default=False,
                        help='Delete the bond table in the wireless programmer')
    parser.add_argument('--library-path', type=pathlib.Path, default=None,
                        help='Path to the product library to load and use (optional)')

    args = parser.parse_args()
    if args.sdk_root is not None:
        os.environ['SD_SDK_ROOT'] = str(args.sdk_root)

    if args.programmer.upper() == 'NOAHLINK':
        assert args.noahlink_driver_path is not None, "Path to the NOAHLink wireless drivers was not set!"
        assert args.noahlink_driver_path.exists() and args.noahlink_driver_path.is_dir(), "Invalid NOAHLink Wireless driver path!"

    return args

def run():
    args = parse_command_line_arguments()

    # NOTE: We must parse the command line arguments to set SD_SDK_ROOT before
    #       importing the DemoApp
    from wireless_demo.demo_ui import DemoApp

    app = DemoApp(args)
    app.run()


if __name__ == '__main__':
    run()
