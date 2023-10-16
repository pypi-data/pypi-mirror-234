import argparse
import configparser
import os
import shutil
import textwrap
import warnings
from getpass import getpass
from typing import List, Optional, Union

from prettytable import PrettyTable

import tetra_hub as hub
from tetra_hub.public_rest_api import TETRA_CLIENT_ENV, _get_token, get_config_path

from .client import SourceModel

_HUB_URL = "https://hub.tetra.ai"


def set_config_path(profile_name: str) -> None:
    os.environ[TETRA_CLIENT_ENV] = f"~/.tetra/{profile_name}.ini"


def add_device_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--device",
        action="store",
        help="Device name",
        required=False,
    )
    parser.add_argument(
        "--device-attr",
        action="append",
        help="Device attribute. This may be repeated for multiple attributes.",
        required=False,
    )
    parser.add_argument(
        "--device-os",
        action="store",
        help="Device OS version",
        required=False,
    )


def get_cli_parser() -> argparse.ArgumentParser:
    # Main CLI arguments
    main_parser = argparse.ArgumentParser(description="CLI interface for tetra-hub")
    subparsers = main_parser.add_subparsers(dest="command")

    # Parser for configure command
    config_parser = subparsers.add_parser(
        "configure", help="Configure tetra-hub client"
    )
    list_devices_parser = subparsers.add_parser(
        "list-devices", help="List available devices"
    )
    submit_profile_cmd = "submit-profile"
    cmd_name = f"tetra-hub {submit_profile_cmd}"
    epilog = textwrap.dedent(
        f"""
    examples:

      # Submit Torchscript model
      {cmd_name} --model resnet50.pt --input_shapes '{{"x": (1, 3, 224, 224)}}' --device "Samsung Galaxy S23"

      # Re-submit existing job
      {cmd_name} --clone np1wlnlg

      # Re-submit with modifications
      {cmd_name} --clone np1wlnlg --options " --compute_unit cpu"
    """
    )
    profile_parser = subparsers.add_parser(
        submit_profile_cmd,
        help="Submit profile job",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # arguments for list-devices
    main_parser.add_argument(
        "--profile",
        action="store",
        help="Alternate client profile. Translates to ~/.tetra/PROFILE.ini.",
        required=False,
    )

    # arguments for list-devices
    add_device_filters(list_devices_parser)

    # arguments for profile
    add_device_filters(profile_parser)
    profile_parser.add_argument(
        "--clone",
        metavar="JOB_ID",
        action="store",
        help="Uses this job as template (any argument can be overridden)",
        required=False,
    )
    profile_parser.add_argument(
        "--model",
        action="store",
        help="Model",
        required=False,
    )
    profile_parser.add_argument(
        "--input_shapes",
        action="store",
        help="Input shapes",
        required=False,
    )
    profile_parser.add_argument(
        "--options",
        action="store",
        help="Job options",
        required=False,
    )
    profile_parser.add_argument(
        "--name",
        action="store",
        help="Optional job name",
        required=False,
    )

    # arguments for configure
    config_parser.add_argument(
        "--api_token",
        action="store",
        help=f"API token (from the accounts page of {_HUB_URL})",
        required=False,
    )
    config_parser.add_argument(
        "--email",
        action="store",
        help="Tetra Hub account email address",
        required=False,
    )
    config_parser.add_argument(
        "--password",
        action="store",
        help="Hub account password",
        required=False,
    )
    config_parser.add_argument(
        "--api_url",
        action="store",
        help=argparse.SUPPRESS,
        default=_HUB_URL,
    )
    config_parser.add_argument(
        "--web_url",
        action="store",
        help=argparse.SUPPRESS,
        default=_HUB_URL,
    )
    config_parser.add_argument("--verbose", action="store_true")
    config_parser.add_argument("--no-verbose", dest="verbose", action="store_false")
    config_parser.set_defaults(verbose=True)

    # Return the argument parser
    return main_parser


def configure(config_data: dict, tetra_config_ini_path: str) -> None:
    # Make a backup if it exists
    if os.path.exists(tetra_config_ini_path):
        backup_tetra_config = f"{tetra_config_ini_path}.bak"
        warnings.warn(
            f"Overwriting configuration: {tetra_config_ini_path} (previous configuration saved to {backup_tetra_config})"
        )
        shutil.copy(tetra_config_ini_path, backup_tetra_config)

    # Create a configuration
    config = configparser.ConfigParser()
    for section in config_data:
        config.add_section(section)
        for key, value in config_data[section].items():
            config.set(section, key, value)

    # Create and save the file
    os.makedirs(os.path.dirname(tetra_config_ini_path), exist_ok=True)
    with open(tetra_config_ini_path, "w") as configfile:
        config.write(configfile)

    # Let the user know they are ready to go.
    print(f"tetra-hub configuration saved to {tetra_config_ini_path}")
    print("=" * 20, f"{tetra_config_ini_path}", "=" * 20)
    with open(tetra_config_ini_path, "r") as configfile:
        print(configfile.read())


class DeviceParams:
    name: str = ""
    os: str = ""
    attrs: List[str] = []

    def is_default(self):
        return not self.name and not self.os and not self.attrs


def parse_device(args: argparse.Namespace) -> DeviceParams:
    params = DeviceParams()

    if args.device:
        params.name = args.device
    if args.device_os:
        params.os = args.device_os
    if args.device_attr:
        params.attrs = args.device_attr

    return params


def parse_input_shapes(
    input_shapes_str: str,
) -> Optional[hub.InputSpecs]:
    if not input_shapes_str:
        return None

    input_shapes = None
    if input_shapes_str:
        try:
            input_shapes = eval(input_shapes_str)
        except Exception:
            raise RuntimeError(
                f"Unable to parse input_shapes as dictionary: {input_shapes_str}"
            )
    return input_shapes


def list_devices(device: DeviceParams) -> None:
    devices = hub.get_devices(
        name=device.name,
        os=device.os,
        attributes=device.attrs,
    )
    table = PrettyTable()
    table.field_names = [
        "Device",
        "OS",
        "Vendor",
        "Type",
        "Chipset",
        "CLI Invocation",
    ]
    for d in devices:
        attr_dict = dict([i.split(":") for i in d.attributes])
        table.add_row(
            [
                d.name,
                f"{attr_dict.get('os', '')} {d.os}",
                f"{attr_dict.get('vendor', '').title()}",
                f"{attr_dict.get('format', '').title()}",
                f"{attr_dict.get('chipset', '')}",
                f'--device "{d.name}" --device-os {d.os}',
            ]
        )
    print(table)


def get_device(device: DeviceParams) -> hub.Device:
    return hub.Device(name=device.name, os=device.os, attributes=device.attrs)


def profile(
    model: Union[SourceModel, str],
    input_shapes: Optional[hub.InputSpecs],
    device: hub.Device,
    name: Optional[str],
    options: str,
) -> None:
    hub.submit_profile_job(
        model=model,
        name=name,
        input_shapes=input_shapes,
        device=device,
        options=options,
    )


def run_cli(args: argparse.Namespace) -> None:
    if args.profile:
        set_config_path(args.profile)

    if args.command == "configure":
        # Data to write to the configuration file
        if args.api_token is None:
            if not args.email:
                args.email = input("Tetra Hub account email address:")
            if not args.password:
                args.password = getpass()
            args.api_token = _get_token(args.api_url, args.email, args.password)

        config_data: dict = {
            "api": {
                "api_token": args.api_token,
                "api_url": args.api_url,
                "web_url": args.web_url,
                "verbose": str(args.verbose),
            }
        }

        # Location for the config file
        config_path: str = get_config_path()

        # Configure
        configure(config_data, config_path)

    elif args.command == "list-devices":
        list_devices(parse_device(args))

    elif args.command == "submit-profile":
        clone_job: Optional[hub.ProfileJob] = None
        if args.clone is not None:
            maybe_clone_job = hub.get_job(args.clone)
            if isinstance(maybe_clone_job, hub.ProfileJob):
                clone_job = maybe_clone_job
            else:
                raise ValueError("Cloned job has to be a profile job")

        options: str = ""
        name: Optional[str] = None
        model: Union[SourceModel, str] = ""
        input_shapes: Optional[hub.InputSpecs] = None
        if args.options:
            options = args.options
        elif clone_job is not None:
            options = clone_job.options
        if args.name:
            name = args.name
        elif clone_job is not None:
            name = clone_job.name

        device_params = parse_device(args)
        # Only fall-back to clone job device if no device info is provided
        if device_params.is_default() and clone_job is not None:
            device = clone_job.device
        else:
            device = get_device(device_params)

        if args.input_shapes:
            input_shapes = parse_input_shapes(args.input_shapes)
        elif clone_job is not None:
            input_shapes = clone_job.shapes

        if args.model:
            model = args.model
        elif clone_job is not None:
            model = clone_job.model
        else:
            raise ValueError("--model (or --clone) must be specified.")

        profile(
            model=model,
            name=name,
            input_shapes=input_shapes,
            device=device,
            options=options,
        )

    else:
        get_cli_parser().print_help()


def main() -> None:
    # Parse command line arguments
    main_parser = get_cli_parser()
    args = main_parser.parse_args()
    run_cli(args)
