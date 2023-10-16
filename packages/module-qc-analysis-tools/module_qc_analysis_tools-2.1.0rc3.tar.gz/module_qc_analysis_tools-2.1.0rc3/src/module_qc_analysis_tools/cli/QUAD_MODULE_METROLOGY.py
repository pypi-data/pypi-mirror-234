from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from statistics import mean

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
    log.info(" \tPerforming QUAD_MODULE_METROLOGY analysis")
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
            if metadata is None:
                metadata = results.get("Metadata")

            module_name = d.get("serialNumber")
            meas = results.get("Measurements")
            # alternatively, props.get("MODULE_SN")

            """ input data """
            results["PCB_BAREMODULE_POSITION_TOP_RIGHT"] = meas.get(
                "PCB_BAREMODULE_POSITION_TOP_RIGHT"
            )
            results["PCB_BAREMODULE_POSITION_BOTTOM_LEFT"] = meas.get(
                "PCB_BAREMODULE_POSITION_BOTTOM_LEFT"
            )
            results["ANGLE_PCB_BM"] = meas.get("ANGLE_PCB_BM")
            thickness = meas.get("AVERAGE_THICKNESS")

            if isinstance(thickness, list) is True:
                results["AVERAGE_THICKNESS"] = thickness
            else:
                pickuparea1 = []
                pickuparea2 = []
                pickuparea3 = []
                pickuparea4 = []
                for i in range(len(thickness)):
                    for k in range(4):
                        if k == 0:
                            pickuparea1.append(thickness[i][k])
                        if k == 1:
                            pickuparea2.append(thickness[i][k])
                        if k == 2:
                            pickuparea3.append(thickness[i][k])
                        if k == 3:
                            pickuparea4.append(thickness[i][k])
                ave_pickuparea = (
                    [mean(pickuparea1)]
                    + [mean(pickuparea2)]
                    + [mean(pickuparea3)]
                    + [mean(pickuparea4)]
                )
                results["AVERAGE_THICKNESS"] = ave_pickuparea
            results["STD_DEVIATION_THICKNESS"] = meas.get("STD_DEVIATION_THICKNESS")
            results["THICKNESS_VARIATION_PICKUP_AREA"] = meas.get(
                "THICKNESS_VARIATION_PICKUP_AREA"
            )
            results["THICKNESS_INCLUDING_POWER_CONNECTOR"] = meas.get(
                "THICKNESS_INCLUDING_POWER_CONNECTOR"
            )
            results["HV_CAPACITOR_THICKNESS"] = meas.get("HV_CAPACITOR_THICKNESS")

            """ Simplistic QC criteria """
            a = 0
            for i in results["AVERAGE_THICKNESS"]:
                if i < 0.2 or i > 0.3:
                    log.info("average thickness is not good")
                    a += -1
            if (
                results["THICKNESS_INCLUDING_POWER_CONNECTOR"] < 1.521
                or results["THICKNESS_INCLUDING_POWER_CONNECTOR"] > 1.761
            ):
                log.info("power connector thickness is not good")
                a += -1
            if (
                results["HV_CAPACITOR_THICKNESS"] < 1.701
                or results["HV_CAPACITOR_THICKNESS"] > 2.111
            ):
                log.info("HV_capacitor thickness is not good")
                a += -1
            if (
                results["PCB_BAREMODULE_POSITION_TOP_RIGHT"][0] < 2.112
                or results["PCB_BAREMODULE_POSITION_TOP_RIGHT"][0] > 2.312
            ):
                log.info("position top is not good")
                a += -1
            if (
                results["PCB_BAREMODULE_POSITION_TOP_RIGHT"][1] < 0.650
                or results["PCB_BAREMODULE_POSITION_TOP_RIGHT"][1] > 0.850
            ):
                log.info("position right is not good")
                a += -1
            if (
                results["PCB_BAREMODULE_POSITION_BOTTOM_LEFT"][0] < 2.112
                or results["PCB_BAREMODULE_POSITION_BOTTOM_LEFT"][0] > 2.312
            ):
                log.info("position bottom is not good")
                a += -1
            if (
                results["PCB_BAREMODULE_POSITION_BOTTOM_LEFT"][1] < 0.650
                or results["PCB_BAREMODULE_POSITION_BOTTOM_LEFT"][1] > 0.850
            ):
                log.info("position left is not good")
                a += -1
            if results["THICKNESS_VARIATION_PICKUP_AREA"] > 0.025:
                log.info("Thickness variation pickup area is not good")
                a += -1

            passes_qc = a == 0

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
                    "DOMINANT_DEFECT",
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
