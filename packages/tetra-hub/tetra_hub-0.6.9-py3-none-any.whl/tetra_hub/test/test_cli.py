import configparser
import os
import tempfile
from datetime import datetime
from unittest import mock

import pytest

import tetra_hub
from tetra_hub._cli import configure, get_cli_parser, parse_input_shapes, run_cli


@pytest.fixture
def config_data():
    config_data = {
        "api": {
            "api_token": "API_TOKEN_fbajc",
            "api_url": "https://staging.tetra.ai",
            "web_url": "https://staging.tetra.ai",
        }
    }
    return config_data


def validate_good_configuration(config):
    assert config.sections() == ["api"]
    assert config.get("api", "api_url") == "https://staging.tetra.ai"
    assert config.get("api", "web_url") == "https://staging.tetra.ai"
    assert config.get("api", "api_token") == "API_TOKEN_fbajc"
    assert set(config["api"].keys()) == set(["api_url", "web_url", "api_token"])


def test_good_configuration(config_data):
    ini_path = tempfile.NamedTemporaryFile(suffix="config.ini").name
    configure(config_data, ini_path)

    # Now read the configuration back
    config = configparser.ConfigParser()
    config.read(ini_path)

    # Validate
    validate_good_configuration(config)


def test_backup_config(config_data):
    ini_path = tempfile.NamedTemporaryFile(suffix="config.ini").name
    configure(config_data, ini_path)
    config_data["api"]["api_token"] = "NEW_API_TOKEN_fbajc"
    configure(config_data, ini_path)

    # Now read the configuration back
    config_bak = configparser.ConfigParser()
    config_bak.read(f"{ini_path}.bak")
    validate_good_configuration(config_bak)

    # Validate
    config = configparser.ConfigParser()
    config.read(ini_path)
    assert config.get("api", "api_token") == "NEW_API_TOKEN_fbajc"


@mock.patch.dict(os.environ, {"TETRA_CLIENT_INI": ""}, clear=True)
def test_named_profile():
    args = get_cli_parser().parse_args(["--profile", "dummy"])
    run_cli(args)
    assert os.environ["TETRA_CLIENT_INI"] == "~/.tetra/dummy.ini"


@pytest.mark.parametrize(
    "input_args, expected_results",
    [
        ([], dict(name="", os="", attributes=[])),
        (
            ["--device", "Apple iPhone 14"],
            dict(name="Apple iPhone 14", os="", attributes=[]),
        ),
        (
            ["--device-os", "ios"],
            dict(name="", os="ios", attributes=[]),
        ),
        (
            ["--device-attr", "chipset:apple-a15"],
            dict(name="", os="", attributes=["chipset:apple-a15"]),
        ),
        (
            ["--device-attr", "chipset:apple-a15", "--device-attr", "framework:coreml"],
            dict(name="", os="", attributes=["chipset:apple-a15", "framework:coreml"]),
        ),
    ],
)
def test_list_devices(input_args, expected_results):
    devices = [
        tetra_hub.Device(
            name="Apple iPhone 14",
            os="16.1",
            attributes=[
                "vendor:apple",
                "os:ios",
                "framework:coreml",
                "chipset:apple-a15",
                "format:phone",
            ],
        ),
        tetra_hub.Device(
            name="Apple iPhone 14 Plus",
            os="16.1",
            attributes=[
                "vendor:apple",
                "os:ios",
                "framework:coreml",
                "chipset:apple-a15",
                "format:phone",
            ],
        ),
    ]
    mock_get_devices = mock.create_autospec(tetra_hub.get_devices, return_value=devices)
    with mock.patch("tetra_hub.get_devices", mock_get_devices):
        args = get_cli_parser().parse_args(["list-devices"] + input_args)
        run_cli(args)
        mock_get_devices.assert_called_once_with(**expected_results)


@pytest.mark.parametrize(
    "input_args, expected_results",
    [
        (
            ["--device", "android", "--model", "model.tflite", "--options", "blah"],
            dict(
                model="model.tflite",
                name=None,
                options="blah",
                input_shapes=None,
                device=tetra_hub.Device("android"),
            ),
        ),
        (
            ["--device", "android", "--model", "model.tflite"],
            dict(
                model="model.tflite",
                name=None,
                options="",
                input_shapes=None,
                device=tetra_hub.Device("android"),
            ),
        ),
        (
            [
                "--device",
                "android",
                "--model",
                "model.tflite",
                "--input_shapes",
                "{'a': (1, 224, 224), 'b': (20, 20)}",
            ],
            dict(
                model="model.tflite",
                name=None,
                options="",
                input_shapes={"a": (1, 224, 224), "b": (20, 20)},
                device=tetra_hub.Device("android"),
            ),
        ),
        (
            [
                "--device",
                "android",
                "--model",
                "model.tflite",
                "--input_shapes",
                "{'a': (1, 224, 224)}",
            ],
            dict(
                model="model.tflite",
                name=None,
                options="",
                input_shapes={"a": (1, 224, 224)},
                device=tetra_hub.Device("android"),
            ),
        ),
        (
            [
                "--device",
                "android",
                "--model",
                "model.tflite",
                "--name",
                "fancy_tflite",
                "--input_shapes",
                "{'a': (1, 224, 224)}",
            ],
            dict(
                model="model.tflite",
                name="fancy_tflite",
                options="",
                input_shapes={"a": (1, 224, 224)},
                device=tetra_hub.Device("android"),
            ),
        ),
        (
            [
                "--clone",
                "abcd1234",
                "--name",
                "fancy_tflite_override",
            ],
            dict(
                model="model.tflite",
                name="fancy_tflite_override",
                options="",
                input_shapes={"a": (1, 224, 224)},
                device=tetra_hub.Device("android"),
            ),
        ),
        (
            [
                "--clone",
                "abcd1234",
                "--model",
                "model_override.tflite",
                "--options",
                "--compute_unit cpu",
                "--device",
                "android_override",
            ],
            dict(
                model="model_override.tflite",
                name="fancy_tflite",
                options="--compute_unit cpu",
                input_shapes={"a": (1, 224, 224)},
                device=tetra_hub.Device("android_override"),
            ),
        ),
    ],
)
def test_profile_job(input_args, expected_results):
    mock_submit_profile_job = mock.create_autospec(
        tetra_hub.submit_profile_job, return_value=None
    )

    def mock_get_job(job_id):
        assert job_id == "abcd1234"
        ret = mock.Mock(
            spec=tetra_hub.ProfileJob,
            job_id=job_id,
            device=tetra_hub.Device("android"),
            model="model.tflite",  # string for ease of testing
            target_model=None,
            date=datetime.now(),
            options="",
            verbose=False,
            shapes={"a": (1, 224, 224)},
        )
        # Mock uses name= argument for something else
        ret.name = "fancy_tflite"
        return ret

    with mock.patch(
        "tetra_hub.submit_profile_job", mock_submit_profile_job
    ), mock.patch("tetra_hub.get_job", mock_get_job):
        args = get_cli_parser().parse_args(
            ["submit-profile"] + input_args,
        )
        run_cli(args)
        mock_submit_profile_job.assert_called_once_with(**expected_results)


@pytest.mark.parametrize(
    "input_args, exp_input_shapes",
    [
        ("{'a': [1, 224, 224]}", {"a": [1, 224, 224]}),
        ("{'a': [1, 224, 224], 'b': (2, 20)}", {"a": [1, 224, 224], "b": (2, 20)}),
    ],
)
def test_parse_input_shapes(input_args, exp_input_shapes):
    args = get_cli_parser().parse_args(
        [
            "submit-profile",
            "--input_shapes",
            input_args,
            "--device",
            "android",
            "--model",
            "model.tflite",
        ]
    )
    input_shapes = parse_input_shapes(args.input_shapes)
    assert input_shapes == exp_input_shapes
