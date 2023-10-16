from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from statistics import stdev

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
    base_output_dir: Path = OPTIONS["output_dir"],
    # qc_criteria_path: Path = OPTIONS["qc_criteria"],
    # layer: str = OPTIONS["layer"],
    verbosity: LogLevel = OPTIONS["verbosity"],
):
    log = logging.getLogger(__name__)
    log.setLevel(verbosity.value)

    log.info("")
    log.info(" ===============================================")
    log.info(" \tPerforming WIREBOND_PULL_TEST analysis")
    log.info(" ===============================================")
    log.info("")

    test_type = Path(__file__).stem

    time_start = round(datetime.timestamp(datetime.now()))
    output_dir = base_output_dir.joinpath(test_type).joinpath(f"{time_start}")
    output_dir.mkdir(parents=True, exist_ok=False)

    allinputs = get_inputs(input_meas)
    # qc_config = get_qc_config(qc_criteria_path, test_type)

    # alloutput = []
    # timestamps = []
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

            module_name = d.get("serialNumber")

            """ Simplistic QC criteria """
            meas_array = metadata.get("pull_data")
            WIRE_PULLS = len(meas_array)
            results["WIRE_PULLS"] = WIRE_PULLS
            strength = []
            counter_of_weak_wire = 0
            counter_of_FE = 0
            counter_of_PCB = 0
            counter_of_bond_peel = 0
            for i in range(WIRE_PULLS):
                each_wire_strength = meas_array[i].get("strength")
                type_of_break = meas_array[i].get("break_mode")
                if each_wire_strength < 5.0:
                    counter_of_weak_wire += 1
                if type_of_break == "Heel break on chip":
                    counter_of_FE += 1
                elif type_of_break == "Heel break on hybrid":
                    counter_of_PCB += 1
                elif type_of_break in ("Bond peel on chip", "Bond peel on hybrid"):
                    counter_of_bond_peel += 1
                strength.append(each_wire_strength)
            results["PULL_STRENGTH"] = sum(strength) / WIRE_PULLS
            results["PULL_STRENGTH_ERROR"] = stdev(strength)
            results["WIRE_BREAKS_5G"] = counter_of_weak_wire
            results["PULL_STRENGTH_MIN"] = min(strength)
            results["PULL_STRENGTH_MAX"] = max(strength)
            results["HEEL_BREAKS_ON_FE_CHIP"] = counter_of_FE / WIRE_PULLS * 100
            results["HEEL_BREAKS_ON_PCB"] = counter_of_PCB / WIRE_PULLS * 100
            results["BOND_PEEL"] = counter_of_bond_peel / WIRE_PULLS * 100

            passes_qc = True

            """ Output a json file """
            outputDF = outputDataFrame()
            outputDF.set_test_type(test_type)
            data = qcDataFrame()
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

            outputDF.set_results(data)
            outputDF.set_pass_flag(passes_qc)

            outfile = output_dir.joinpath(f"{module_name}.json")
            log.info(f" Saving output of analysis to: {outfile}")
            out = outputDF.to_dict(True)
            out.update({"serialNumber": module_name})
            save_dict_list(outfile, [out])


#            plt_outfile = output_dir.joinpath(f"{module_name}_plot.png")
#           fig.savefig(plt_outfile, dpi=150)


if __name__ == "__main__":
    typer.run(main)
