from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import numpy as np
import typer
from module_qc_data_tools import (
    get_layer_from_sn,
    load_json,
    outputDataFrame,
    qcDataFrame,
    save_dict_list,
)

from module_qc_analysis_tools import __version__
from module_qc_analysis_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_analysis_tools.utils.analysis import (
    check_layer,
    perform_qc_analysis,
    print_result_summary,
    submit_results,
)
from module_qc_analysis_tools.utils.misc import (
    DataExtractor,
    JsonChecker,
    bcolors,
    get_inputs,
    get_qc_config,
    get_time_stamp,
)

app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    input_meas: Path = OPTIONS["input_meas"],
    base_output_dir: Path = OPTIONS["output_dir"],
    qc_criteria_path: Path = OPTIONS["qc_criteria"],
    input_layer: str = OPTIONS["layer"],
    permodule: bool = OPTIONS["permodule"],
    submit: bool = OPTIONS["submit"],
    site: str = OPTIONS["site"],
    verbosity: LogLevel = OPTIONS["verbosity"],
):
    test_type = Path(__file__).stem

    allinputs = get_inputs(input_meas)
    qc_config = get_qc_config(qc_criteria_path, test_type)

    time_start = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_dir = base_output_dir.joinpath(test_type).joinpath(f"{time_start}")
    output_dir.mkdir(parents=True, exist_ok=False)

    log = logging.getLogger("analysis")
    log.setLevel(verbosity.value)
    log.addHandler(logging.FileHandler(f"{output_dir}/output.log"))

    log.info("")
    log.info(" =======================================")
    log.info(" \tPerforming OVP analysis")
    log.info(" =======================================")
    log.info("")

    alloutput = []
    timestamps = []
    for filename in sorted(allinputs):
        log.info("")
        log.info(f" Loading {filename}")
        meas_timestamp = get_time_stamp(filename)
        inputDFs = load_json(filename)

        log.debug(
            f" There are results from {len(inputDFs)} chip(s) stored in this file"
        )
        for inputDF in inputDFs:
            qcframe = inputDF.get_results()
            metadata = qcframe.get_meta_data()

            if input_layer == "Unknown":
                try:
                    layer = get_layer_from_sn(metadata.get("ModuleSN"))
                except Exception:
                    log.error(bcolors.WARNING + " Something went wrong." + bcolors.ENDC)
            else:
                log.warning(
                    bcolors.WARNING
                    + " Overwriting default layer config {} with manual input {}!".format(
                        get_layer_from_sn(metadata.get("ModuleSN")), input_layer
                    )
                    + bcolors.ENDC
                )
                layer = input_layer
            check_layer(layer)

            """"" Check file integrity  """
            checker = JsonChecker(inputDF, test_type)

            try:
                checker.check()
            except BaseException as exc:
                log.exception(exc)
                log.error(
                    bcolors.ERROR
                    + " JsonChecker check not passed, skipping this input."
                    + bcolors.ENDC
                )
                continue
            else:
                log.debug(" JsonChecker check passed!")
                pass

            try:
                chipname = metadata.get("Name")
                log.debug(f" Found chip name = {chipname} from chip config")
            except Exception:
                log.warning(
                    bcolors.WARNING
                    + "Chip name not found in input from {filename}, skipping."
                    + bcolors.ENDC
                )
                continue

            institution = metadata.get("Institution")
            if site != "" and institution != "":
                log.warning(
                    bcolors.WARNING
                    + " Overwriting default institution {} with manual input {}!".format(
                        institution, site
                    )
                    + bcolors.ENDC
                )
                institution = site
            elif site != "":
                institution = site

            if institution == "":
                log.error(
                    bcolors.ERROR
                    + "No institution found. Please specify your testing site either in the measurement data or specify with the --site option. "
                    + bcolors.ENDC
                )
                return

            """""  Calculate quanties   """
            extractor = DataExtractor(inputDF, test_type)
            calculated_data = extractor.calculate()

            passes_qc = True

            # Load values to dictionary for QC analysis
            results = {}
            results.update({"OVP_VINA": calculated_data["VinA"]["Values"][0]})
            results.update({"OVP_VIND": calculated_data["VinD"]["Values"][0]})
            results.update({"OVP_VREFOVP": calculated_data["VrefOVP"]["Values"][0]})
            results.update({"OVP_IINA": calculated_data["IinA"]["Values"][0]})
            results.update({"OVP_IIND": calculated_data["IinD"]["Values"][0]})

            # Perform QC analysis
            chiplog = logging.FileHandler(f"{output_dir}/{chipname}.log")
            log.addHandler(chiplog)
            passes_qc, summary, rounded_results = perform_qc_analysis(
                test_type, qc_config, layer, results
            )
            print_result_summary(summary, test_type, output_dir, chipname)
            if passes_qc == -1:
                log.error(
                    bcolors.ERROR
                    + f" QC analysis for {chipname} was NOT successful. Please fix and re-run. Continuing to next chip.."
                    + bcolors.ENDC
                )
                continue
            log.info("")
            if passes_qc:
                log.info(
                    f" Chip {chipname} passes QC? "
                    + bcolors.OKGREEN
                    + f"{passes_qc}"
                    + bcolors.ENDC
                )
            else:
                log.info(
                    f" Chip {chipname} passes QC? "
                    + bcolors.BADRED
                    + f"{passes_qc}"
                    + bcolors.ENDC
                )
            log.info("")
            log.removeHandler(chiplog)
            chiplog.close()

            """"" Output a json file """
            outputDF = outputDataFrame()
            outputDF.set_test_type(test_type)
            data = qcDataFrame()
            data._meta_data.update(metadata)
            data.add_property(
                "ANALYSIS_VERSION",
                __version__,
            )
            data.add_meta_data(
                "MEASUREMENT_VERSION",
                qcframe.get_properties().get(test_type + "_MEASUREMENT_VERSION"),
            )
            data.add_meta_data("QC_LAYER", layer)
            data.add_meta_data("INSTITUTION", institution)

            # Add all values used in QC selection to output file
            for key, value in rounded_results.items():
                data.add_parameter(key, value)

            # Load values to store in output file
            outputDF.set_results(data)
            outputDF.set_pass_flag(passes_qc)
            if submit:
                submit_results(
                    outputDF.to_dict(True),
                    time_start,
                    institution,
                    output_dir.joinpath("submit.txt"),
                    layer,
                )
            if permodule:
                alloutput += [outputDF.to_dict(True)]
                timestamps += [meas_timestamp]
            else:
                outfile = output_dir.joinpath(f"{chipname}.json")
                log.info(f" Saving output of analysis to: {outfile}")
                save_dict_list(outfile, [outputDF.to_dict(True)])
    if permodule:
        # Only store results from same timestamp into same file
        dfs = np.array(alloutput)
        tss = np.array(timestamps)
        for x in np.unique(tss):
            outfile = output_dir.joinpath("module.json")
            log.info(f" Saving output of analysis to: {outfile}")
            save_dict_list(
                outfile,
                dfs[tss == x].tolist(),
            )


if __name__ == "__main__":
    typer.run(main)
