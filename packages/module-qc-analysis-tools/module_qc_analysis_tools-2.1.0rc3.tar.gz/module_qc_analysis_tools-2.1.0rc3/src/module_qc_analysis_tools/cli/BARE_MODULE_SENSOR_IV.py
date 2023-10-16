from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import typer
from module_qc_data_tools import (
    __version__,
    load_json,
    outputDataFrame,
    qcDataFrame,
    save_dict_list,
)

from module_qc_analysis_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_analysis_tools.utils.misc import (
    get_inputs,
)

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    input_meas: Path = OPTIONS["input_meas"],
    input_aux: Path = OPTIONS["input_aux.json"],
    base_output_dir: Path = OPTIONS["output_dir"],
    # qc_criteria_path: Path = OPTIONS["qc_criteria"],
    # layer: str = OPTIONS["layer"],
    verbosity: LogLevel = OPTIONS["verbosity"],
):
    log = logging.getLogger(__name__)
    log.setLevel(verbosity.value)

    log.info("")
    log.info(" ===============================================")
    log.info(" \tPerforming BARE_MODULE_SENSOR_IV analysis")
    log.info(" ===============================================")
    log.info("")

    test_type = Path(__file__).stem

    time_start = round(datetime.timestamp(datetime.now()))
    output_dir = base_output_dir.joinpath(test_type).joinpath(f"{time_start}")
    output_dir.mkdir(parents=True, exist_ok=False)

    allinputs = get_inputs(input_meas)
    reference_IV = get_inputs(input_aux)
    # qc_config = get_qc_config(qc_criteria_path, test_type)

    # alloutput = []
    # timestamps = []

    for file in sorted(reference_IV):
        with Path(file).open() as f:
            reference_dict = json.load(f)
        reference = reference_dict.get("reference_IVs")
        reference_sensor_IV = reference[0]
        reference_bare_IV = reference[1]

    for filename in sorted(allinputs):
        log.info("")
        log.info(f" Loading {filename}")
        # meas_timestamp = get_time_stamp(filename)

        inputDFs = load_json(filename)
        log.info(
            f" There are results from {len(inputDFs)} module(s) stored in this file"
        )

        with Path(filename).open() as f:
            jsonData = json.load(f)

        for j, inputDF in zip(jsonData, inputDFs):
            d = inputDF.to_dict()

            results = j[0].get("results")
            props = results.get("property")
            metadata = results.get("metadata")
            if metadata is None:
                metadata = results.get("Metadata")

            module_name = d.get("serialNumber")

            # ------------------------------------------------------------------
            # Flagging
            Ilc_pre = reference_sensor_IV.get("Ilc")
            Ilc_now = reference_bare_IV.get("Ilc")
            Ilc_flag = Ilc_pre * 2 > Ilc_now
            result_pass_sen = reference_sensor_IV.get("qc_passed")
            result_pass_bare = reference_bare_IV.get("qc_passed")

            passes_qc = Ilc_flag and result_pass_bare and result_pass_sen

            log.info(
                f"Ilc_flag: {Ilc_flag}, result_pass: {result_pass_bare}, result_pass_sen: {result_pass_sen}, passes_qc: {passes_qc}"
            )

            """ Output a json file """
            outputDF = outputDataFrame()
            outputDF.set_test_type(test_type)
            data = qcDataFrame()

            if metadata is not None:
                data._meta_data.update(metadata)
            """ Pass-through properties in input """
            for key, value in props.items():
                data.add_property(key, value)

            """ Add analysis version """
            data.add_property(
                "ANALYSIS_VERSION",
                __version__,
            )
            """ Pass-through measurement parameters """
            for key, value in results.items():
                if key in [
                    "property",
                    "metadata",
                    "Metadata",
                    "Measurements",
                    "comment",
                ]:
                    continue

                data.add_parameter(key, value)

            for key, value in results["Measurements"].items():
                data.add_parameter(key, value)
            outputDF.set_results(data)
            outputDF.set_pass_flag(passes_qc)

            outfile = output_dir.joinpath(f"{module_name}.json")
            log.info(f" Saving output of analysis to: {outfile}")
            out = outputDF.to_dict(True)
            out.update({"serialNumber": module_name})
            save_dict_list(outfile, [out])


if __name__ == "__main__":
    typer.run(main)
