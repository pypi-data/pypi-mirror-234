from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from module_qc_analysis_tools.cli import app


@pytest.fixture()
def base_path():
    return Path("") / "module-qc-tools" / "emulator" / "outputs" / "Measurements"


@pytest.fixture()
def data_path():
    return Path("") / "src" / "module_qc_analysis_tools" / "data"


@pytest.fixture()
def runner():
    return CliRunner(mix_stderr=False)


def test_adc_calibration(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "adc-calibration",
            "-i",
            base_path.joinpath("ADC_CALIBRATION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? True" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_analog_readback(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "analog-readback",
            "-i",
            base_path.joinpath("ANALOG_READBACK/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_vcal_calibration(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "vcal-calibration",
            "-i",
            base_path.joinpath("VCAL_CALIBRATION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? True" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_sldo(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "sldo",
            "-i",
            base_path.joinpath("SLDO/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_injection_capacitance(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "injection-capacitance",
            "-i",
            base_path.joinpath("INJECTION_CAPACITANCE/1000000001/"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_lp_mode(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "lp-mode",
            "-i",
            base_path.joinpath("LP_MODE/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_ov_protection(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "overvoltage-protection",
            "-i",
            base_path.joinpath("OVERVOLTAGE_PROTECTION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_undershunt_protection(runner, base_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "undershunt-protection",
            "-i",
            base_path.joinpath("UNDERSHUNT_PROTECTION/1000000001//"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    for chip_id in range(1, 5):
        assert (
            f"Chip dummy_chip{chip_id} passes QC? False" in caplog.text
        ), f"Failure for chip {chip_id}"


def test_minimum_health(runner, data_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "min-health-test",
            "-i",
            data_path.joinpath("example_scans/info_TEST.json"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        caplog.text.count("Saving output of analysis to") == 4
    ), "Minimum health test failed."


def test_tuning(runner, data_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "tuning",
            "-i",
            data_path.joinpath("example_scans/info_TEST.json"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert caplog.text.count("Saving output of analysis to") == 4, "Tuning test failed."


def test_pixel_failure(runner, data_path, caplog):
    result = runner.invoke(
        app,
        args=[
            "analysis",
            "pixel-failure-analysis",
            "-i",
            data_path.joinpath("example_scans/info_TEST.json"),
            "-v",
            "DEBUG",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stderr
    assert (
        caplog.text.count("Saving output of analysis to") == 4
    ), "Pixel failure analysis test failed."
