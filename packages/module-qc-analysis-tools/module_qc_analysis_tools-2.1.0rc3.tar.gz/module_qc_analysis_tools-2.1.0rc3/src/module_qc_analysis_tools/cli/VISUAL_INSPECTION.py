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
    base_output_dir: Path = OPTIONS["output_dir"],
    # qc_criteria_path: Path = OPTIONS["qc_criteria"],
    # layer: str = OPTIONS["layer"],
    verbosity: LogLevel = OPTIONS["verbosity"],
):
    log = logging.getLogger(__name__)
    log.setLevel(verbosity.value)

    log.info("")
    log.info(" ===============================================")
    log.info(" \tPerforming VISUAL_INSPECTION analysis")
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

            # stage = j[0].get("stage")
            results = j[0].get("results")
            props = results.get("property")
            metadata = results.get("metadata")

            module_name = d.get("serialNumber")
            # alternatively, props.get("MODULE_SN")

            qc = {
                "SMD_COMPONENTS_PASSED_QC": 1,
                "SENSOR_CONDITION_PASSED_QC": 1,
                "FE_CHIP_CONDITION_PASSED_QC": 1,
                "GLUE_DISTRIBUTION_PASSED_QC": 1,
                "WIREBONDING_PASSED_QC": 1,
                "PARYLENE_COATING_PASSED_QC": 1,
            }

            front_defects = metadata.get("front_defects")
            back_defects = metadata.get("back_defects")

            for defect_results in [front_defects, back_defects]:
                if defect_results is None:
                    continue

                for _tile, defects in defect_results.items():
                    for defect in defects:
                        keymap = {
                            "glue": "GLUE_DISTRIBUTION_PASSED_QC",
                            "wire": "WIREBONDING_PASSED_QC",
                            "_sensor": "SENSOR_CONDITION_PASSED_QC",
                            "_fe": "FE_CHIP_CONDITION_PASSED_QC",
                            "_pcb": "SMD_COMPONENTS_PASSED_QC",
                            "parylene": "PARYLENE_COATING_PASSED_QC",
                        }

                        defect_level = 1

                        if defect.lower().find("yellow") >= 0:
                            defect_level = 2
                        elif defect.lower().find("red") >= 0:
                            defect_level = 3

                        for key, dtype in keymap.items():
                            if defect.lower().find(key) >= 0:
                                qc[dtype] = defect_level
                                break

            """ Simplistic QC criteria """
            passes_qc = True

            for key, value in qc.items():
                key
                if value >= 3:
                    passes_qc = False
                    break

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
            for key, value in qc.items():
                data.add_parameter(key, value)

            att = {}
            if metadata.get("front_defect_images") is not None:
                for tile, img_id in metadata.get("front_defect_images").items():
                    name = f"front_tile{tile}.jpg"
                    att[name] = img_id
            if metadata.get("back_defect_images") is not None:
                for tile, img_id in metadata.get("back_defect_images").items():
                    name = f"back_tile{tile}.jpg"
                    att[name] = img_id

            outputDF.set_results(data)
            outputDF.set_pass_flag(passes_qc)

            outfile = output_dir.joinpath(f"{module_name}.json")
            log.info(f" Saving output of analysis to: {outfile}")
            out = outputDF.to_dict(True)
            out.update({"serialNumber": module_name})
            out.update({"gridfs_attachments": att})

            save_dict_list(outfile, [out])


if __name__ == "__main__":
    typer.run(main)
