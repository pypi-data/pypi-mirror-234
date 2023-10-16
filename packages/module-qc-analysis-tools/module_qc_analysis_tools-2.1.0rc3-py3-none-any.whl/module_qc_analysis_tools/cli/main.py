"""
Top-level entrypoint for the command line interface.
"""
from __future__ import annotations

import typer

import module_qc_analysis_tools
from module_qc_analysis_tools.cli.ADC_CALIBRATION import main as adc_calibration
from module_qc_analysis_tools.cli.ANALOG_READBACK import main as analog_readback
from module_qc_analysis_tools.cli.BARE_MODULE_SENSOR_IV import (
    main as bare_module_sensor_iv,
)
from module_qc_analysis_tools.cli.globals import CONTEXT_SETTINGS
from module_qc_analysis_tools.cli.GLUE_MODULE_FLEX_ATTACH import (
    main as glue_module_flex_attach,
)
from module_qc_analysis_tools.cli.INJECTION_CAPACITANCE import (
    main as injection_capacitance,
)
from module_qc_analysis_tools.cli.IV_MEASURE import main as iv_measure
from module_qc_analysis_tools.cli.load_yarr_scans import main as load_yarr_scans
from module_qc_analysis_tools.cli.LP_MODE import main as lp_mode
from module_qc_analysis_tools.cli.MASS_MEASUREMENT import main as mass
from module_qc_analysis_tools.cli.MIN_HEALTH_TEST import main as min_health_test
from module_qc_analysis_tools.cli.OVERVOLTAGE_PROTECTION import (
    main as overvoltage_protection,
)
from module_qc_analysis_tools.cli.overwrite_config import main as overwrite_config
from module_qc_analysis_tools.cli.PARYLENE import main as parylene
from module_qc_analysis_tools.cli.PIXEL_FAILURE_ANALYSIS import (
    main as pixel_failure_analysis,
)
from module_qc_analysis_tools.cli.SLDO import main as sldo
from module_qc_analysis_tools.cli.TUNING import main as tuning
from module_qc_analysis_tools.cli.UNDERSHUNT_PROTECTION import (
    main as undershunt_protection,
)
from module_qc_analysis_tools.cli.update_chip_config import main as update_chip_config
from module_qc_analysis_tools.cli.VCAL_CALIBRATION import main as vcal_calibration
from module_qc_analysis_tools.cli.VISUAL_INSPECTION import main as visual_inspection
from module_qc_analysis_tools.cli.WIREBOND_PULL_TEST import main as wirebond_pull_test
from module_qc_analysis_tools.cli.WIREBONDING_INFORMATION import (
    main as wirebonding_information,
)

# subcommands
app = typer.Typer(context_settings=CONTEXT_SETTINGS)
app_analysis = typer.Typer(context_settings=CONTEXT_SETTINGS)
app_config = typer.Typer(context_settings=CONTEXT_SETTINGS)
app.add_typer(app_analysis, name="analysis")
app.add_typer(app_config, name="config")


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", help="Print the current version."),
    prefix: bool = typer.Option(
        False, "--prefix", help="Print the path prefix for data files."
    ),
) -> None:
    """
    Manage top-level options
    """
    if version:
        typer.echo(f"module-qc-analysis-tools v{module_qc_analysis_tools.__version__}")
        raise typer.Exit()
    if prefix:
        typer.echo(module_qc_analysis_tools.data.resolve())
        raise typer.Exit()


app_analysis.command("adc-calibration")(adc_calibration)
app_analysis.command("analog-readback")(analog_readback)
app_analysis.command("injection-capacitance")(injection_capacitance)
app_analysis.command("sldo")(sldo)
app_analysis.command("vcal-calibration")(vcal_calibration)
app_analysis.command("overvoltage-protection")(overvoltage_protection)
app_analysis.command("lp-mode")(lp_mode)
app_analysis.command("mass-measurement")(mass)
app_analysis.command("iv-measure")(iv_measure)
app_analysis.command("visual-inspection")(visual_inspection)
app_analysis.command("wirebond-pull-test")(wirebond_pull_test)
app_analysis.command("wirebonding-information")(wirebonding_information)
app_analysis.command("glue-module-flex-attach")(glue_module_flex_attach)
app_analysis.command("parylene")(parylene)
app_analysis.command("bare-module-sensor-iv")(bare_module_sensor_iv)
app_analysis.command("min-health-test")(min_health_test)
app_analysis.command("tuning")(tuning)
app_analysis.command("pixel-failure-analysis")(pixel_failure_analysis)
app_analysis.command("undershunt-protection")(undershunt_protection)
app_config.command("overwrite")(overwrite_config)
app_config.command("update")(update_chip_config)
app_config.command("load-yarr-scans")(load_yarr_scans)

# for generating documentation using mkdocs-click
typer_click_object = typer.main.get_command(app)
