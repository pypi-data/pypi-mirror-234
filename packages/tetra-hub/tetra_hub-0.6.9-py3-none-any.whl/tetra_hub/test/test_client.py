import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tetra_hub import SourceModelType
from tetra_hub.client import (
    Client,
    Device,
    UserError,
    _assert_is_valid_zipped_model,
    _make_zipped_model_compatible,
)


def create_sample_mlmodelc(modelDir: Path, include_assemble_json: bool = False):
    Path(modelDir).mkdir(parents=True)
    Path(modelDir / "model.espresso.net").touch()
    Path(modelDir / "model.espresso.shape").touch()
    Path(modelDir / "model.espresso.weights").touch()
    if include_assemble_json:
        Path(modelDir / "assemble.json").touch()


def test_valid_zipped_mlmodelc():
    #  1. <filepath>/foo.mlmodelc/assemble.json in case of pipeline model
    #  2. <filepath>/foo.mlmodelc/model.espresso.net or
    #  3. <filepath>/foo.mlmodelc/model0/model.espresso.net in case of pipeline model

    mlmodelc_name = "myModel.mlmodelc"
    # Case 1:
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir, include_assemble_json=True)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Case 2
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Case 3
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / "myModel.mlmodelc"
        pipelinePath = Path(modelDir) / "model0"
        create_sample_mlmodelc(pipelinePath)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Unsupported: model.espresso.net / assemble.json present
    # with flat directory structure i.e. model.zip -> model.espresso.net
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlmodelc_name
        create_sample_mlmodelc(modelDir, include_assemble_json=True)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(str(zipPath), "zip", root_dir=modelDir, base_dir="./")
        with pytest.raises(UserError):
            _assert_is_valid_zipped_model(f"{zipPath}.zip")

    # Valid .mlmodelc within zip with no model.espresso.net/assemble.json
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        # Make an invalid model
        modelDir = Path(baseDir) / mlmodelc_name
        Path(modelDir).mkdir()
        Path(modelDir / "bad_file").touch()

        # Check that this fails
        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlmodelc_name
        )
        with pytest.raises(UserError):
            _assert_is_valid_zipped_model(f"{zipPath}.zip")


def test_valid_zipped_mlpackage():
    # <dirpath>/foo.mlpackage/ in case of zipped mlpackage

    mlpackage_name = "myModel.mlpackage"
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / mlpackage_name
        os.makedirs(modelDir)

        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(
            str(zipPath), "zip", root_dir=baseDir, base_dir=mlpackage_name
        )
        _assert_is_valid_zipped_model(f"{zipPath}.zip")


def test_make_mlmodelc_compatible_zip_does_not_zip_zip():
    model_name = "myModel.mlmodelc"
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / model_name
        create_sample_mlmodelc(model_dir)

        zip_base_path = Path(base_dir) / "my_model_archive"
        zip_path = shutil.make_archive(
            str(zip_base_path), "zip", root_dir=base_dir, base_dir=model_name
        )

        with tempfile.NamedTemporaryFile(suffix=".mlmodelc.zip") as model_zip_tempfile:
            mlmodelc_zip_path = _make_zipped_model_compatible(
                zip_path, model_zip_tempfile.name, ".mlmodelc"
            )
            assert mlmodelc_zip_path == zip_path


def test_make_mlmodelc_compatible_zip_zips_dir():
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / "myModel.mlmodelc"
        create_sample_mlmodelc(model_dir)

        model_output_path = str(Path(base_dir, "output_model_dir"))
        os.makedirs(model_output_path)
        zipfile_path = _make_zipped_model_compatible(
            str(model_dir), model_output_path, ".mlmodelc"
        )
        assert zipfile_path == os.path.join(model_output_path, "myModel.mlmodelc.zip")
        _assert_is_valid_zipped_model(zipfile_path)


def test_make_mlmodelc_compatible_zip_zips_dir_removing_additional_dirs():
    with tempfile.TemporaryDirectory(suffix="baseDir") as base_dir:
        model_dir = Path(base_dir) / "myModel.mlmodelc"
        create_sample_mlmodelc(model_dir)
        Path(os.path.join(base_dir, "__MACOS__")).mkdir(parents=True)
        Path(os.path.join(base_dir, "some_random_file")).touch()

        zipped_file_path = shutil.make_archive(
            os.path.join(base_dir, "test_model.mlmodelc"), "zip", root_dir=base_dir
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            zipfile_path = _make_zipped_model_compatible(
                zipped_file_path, tmp_dir, ".mlmodelc"
            )
            assert zipfile_path == str(os.path.join(tmp_dir, "myModel.mlmodelc.zip"))
            _assert_is_valid_zipped_model(zipfile_path)


@pytest.mark.parametrize(
    "framework, os_type, os_version, model_type, supported",
    [
        # .pt supported on all devices
        ("framework:coreml", "os:macos", "12.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:tflite", "os:macos", "12.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:onnx", "os:macos", "12.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:onnx", "os:ios", "15.1", SourceModelType.TORCHSCRIPT, True),
        ("framework:tflite", "os:android", "10.", SourceModelType.TORCHSCRIPT, True),
        ("framework:onnx", "os:android", "10.1", SourceModelType.TORCHSCRIPT, True),
        # .mlpackage is supported only on iOS15+ and macOS12+
        ("framework:coreml", "os:macos", "12.1", SourceModelType.MLPACKAGE, True),
        ("framework:coreml", "os:macos", "11.1", SourceModelType.MLPACKAGE, False),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.MLPACKAGE, True),
        ("framework:coreml", "os:ios", "13.1", SourceModelType.MLPACKAGE, False),
        ("framework:tflite", "os:android", "10.", SourceModelType.MLPACKAGE, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.MLPACKAGE, False),
        # .mlmodel is supported only on iOS and macOS
        ("framework:coreml", "os:macos", "12.1", SourceModelType.MLMODEL, True),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.MLMODEL, True),
        ("framework:onnx", "os:macos", "12.1", SourceModelType.MLMODEL, False),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.MLMODEL, False),
        ("framework:tflite", "os:android", "10.", SourceModelType.MLMODEL, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.MLMODEL, False),
        # .mlmodelc is supported only on iOS and macOS
        ("framework:coreml", "os:macos", "12.1", SourceModelType.MLMODELC, True),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.MLMODELC, True),
        ("framework:tflite", "os:android", "10.", SourceModelType.MLMODELC, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.MLMODELC, False),
        # .onnx is supported with tflite framework
        ("framework:coreml", "os:macos", "12.1", SourceModelType.ONNX, False),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.ONNX, False),
        ("framework:onnx", "os:macos", "12.1", SourceModelType.ONNX, False),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.ONNX, True),
        ("framework:tflite", "os:android", "10.", SourceModelType.ONNX, True),
        ("framework:onnx", "os:android", "10.1", SourceModelType.ONNX, False),
        # .ort is supported with ONNX runtime
        ("framework:coreml", "os:macos", "12.1", SourceModelType.ORT, False),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.ORT, False),
        ("framework:onnx", "os:macos", "12.1", SourceModelType.ORT, True),
        ("framework:onnx", "os:ios", "15.1", SourceModelType.ORT, True),
        ("framework:tflite", "os:android", "10.", SourceModelType.ORT, False),
        ("framework:onnx", "os:android", "10.1", SourceModelType.ORT, True),
        # .tflite is supported with tflite framework
        ("framework:coreml", "os:macos", "12.1", SourceModelType.TFLITE, False),
        ("framework:coreml", "os:ios", "15.1", SourceModelType.TFLITE, False),
        ("framework:tflite", "os:macos", "12.1", SourceModelType.TFLITE, True),
        ("framework:tflite", "os:ios", "15.1", SourceModelType.TFLITE, True),
        ("framework:tflite", "os:android", "10.", SourceModelType.TFLITE, True),
        ("framework:onnx", "os:android", "10.1", SourceModelType.TFLITE, False),
    ],
)
def test_model_type_device_check(
    framework, os_type, os_version, model_type, supported, monkeypatch
):
    device = Device(attributes=[framework, os_type], os=os_version)
    monkeypatch.setattr(
        Client,
        "_get_device",
        MagicMock(return_value=device),
    )

    client = Client()
    if supported:
        client._check_devices(device, model_type)
    else:
        with pytest.raises(UserError, match=".*does not support.*"):
            client._check_devices(device, model_type)
