from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
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
    FitMethod,
    LogLevel,
)
from module_qc_analysis_tools.utils.analysis import (
    check_layer,
    get_n_chips,
    get_nominal_current,
    get_nominal_RextA,
    get_nominal_RextD,
    get_nominal_Voffs,
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
    linear_fit,
    linear_fit_np,
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
    nChipsInput: int = OPTIONS["nchips"],
    fit_method: FitMethod = OPTIONS["fit_method"],
    verbosity: LogLevel = OPTIONS["verbosity"],
    lp_enable: bool = OPTIONS["lp_enable"],
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

    # Turn off matplotlib DEBUG messages
    plt.set_loglevel(level="warning")

    log.info("")
    log.info(" =======================================")
    log.info(" \tPerforming SLDO analysis")
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
            """Check file integrity"""
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

            """  Get info  """
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

            # SLDO parameters
            RextA = get_nominal_RextA(layer)
            RextD = get_nominal_RextD(layer)
            if nChipsInput == 0:
                nChips = get_n_chips(layer)
            elif nChips != get_n_chips(layer):
                log.warning(
                    bcolors.WARNING
                    + " Overwriting default number of chips ({}) with manual input ({})!".format(
                        get_n_chips(layer), nChipsInput
                    )
                    + bcolors.ENDC
                )
                nChips = nChipsInput

            try:
                kShuntA = (
                    metadata.get("ChipConfigs")
                    .get("RD53B")
                    .get("Parameter")
                    .get("KShuntA")
                )
                log.debug(f" Found kShuntA = {kShuntA} from chip config")
            except Exception:
                log.warning(
                    bcolors.WARNING
                    + " No KShuntA parameter found in chip metadata. Using default KShuntA = 1040"
                    + bcolors.ENDC
                )
                kShuntA = 1040

            try:
                kShuntD = (
                    metadata.get("ChipConfigs")
                    .get("RD53B")
                    .get("Parameter")
                    .get("KShuntD")
                )
                log.debug(f" Found kShuntD = {kShuntD} from chip config")
            except Exception:
                log.warning(
                    bcolors.WARNING
                    + " No KShuntD parameter found in chip metadata. Using default KShuntD = 1040"
                    + bcolors.ENDC
                )
                kShuntD = 1040.0

            try:
                chipname = metadata.get("Name")
                log.debug(f" Found chip name = {chipname} from chip config")
            except Exception:
                log.error(
                    bcolors.ERROR
                    + f" Chip name not found in input from {filename}, skipping."
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

            R_eff = 1.0 / ((kShuntA / RextA) + (kShuntD / RextD)) / nChips

            Vofs = get_nominal_Voffs(layer, lp_enable)

            p = np.poly1d([R_eff, Vofs])
            p1 = np.poly1d([R_eff, 0])

            """  Calculate quanties   """
            extractor = DataExtractor(inputDF, test_type)
            calculated_data = extractor.calculate()

            passes_qc = True

            # Plot parameters
            Iint_max = (
                max(
                    max(calculated_data["Iref"]["Values"] * 100000),
                    max(calculated_data["IcoreD"]["Values"]),
                    max(calculated_data["IcoreA"]["Values"]),
                    max(calculated_data["IshuntD"]["Values"]),
                    max(calculated_data["IshuntA"]["Values"]),
                    max(calculated_data["IinD"]["Values"]),
                    max(calculated_data["IinA"]["Values"]),
                )
                + 0.5
            )
            I_max = max(calculated_data["Current"]["Values"]) + 0.5
            I_min = min(calculated_data["Current"]["Values"]) - 0.5
            V_max = (
                max(
                    max(calculated_data["VrefOVP"]["Values"]),
                    max(calculated_data["Vofs"]["Values"]),
                    max(calculated_data["VDDD"]["Values"]),
                    max(calculated_data["VDDA"]["Values"]),
                    max(calculated_data["VinD"]["Values"]),
                    max(calculated_data["VinA"]["Values"]),
                )
                + 2.0
            )
            T_min = min(0.0, min(calculated_data["Temperature"]["Values"]))
            T_max = max(calculated_data["Temperature"]["Values"]) + 1.0

            # Internal voltages visualization
            fig, ax1 = plt.subplots()
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["VinA"]["Values"],
                marker="o",
                markersize=4,
                label="VinA",
                color="tab:red",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["VinD"]["Values"],
                marker="o",
                markersize=4,
                label="VinD",
                color="tab:red",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["VDDA"]["Values"],
                marker="o",
                markersize=4,
                label="VDDA",
                color="tab:blue",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["VDDD"]["Values"],
                marker="o",
                markersize=4,
                label="VDDD",
                color="tab:blue",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["Vofs"]["Values"],
                marker="o",
                markersize=4,
                label="Vofs",
                color="tab:orange",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["VrefOVP"]["Values"],
                marker="o",
                markersize=4,
                label="VrefOVP",
                color="tab:cyan",
            )

            xp = np.linspace(I_min, I_max, 1000)
            ax1.plot(
                xp,
                p(xp),
                label=f"V = {R_eff:.3f} I + {Vofs:.2f}",
                color="tab:brown",
                linestyle="dotted",
            )
            ax1.set_xlabel("I [A]")
            ax1.set_ylabel("V [V]")
            plt.title(f"VI curve for chip: {chipname}")
            plt.xlim(I_min, I_max)
            ax1.set_ylim(0.0, V_max)
            ax1.legend(loc="upper left", framealpha=0)
            plt.grid()

            ax2 = ax1.twinx()
            ax2.plot(
                calculated_data["Current"]["Values"],
                calculated_data["Temperature"]["Values"],
                marker="^",
                markersize=4,
                color="tab:green",
                label="Temperature (NTC)",
                linestyle="-.",
            )
            ax2.set_ylabel("T [C]")
            ax2.set_ylim(T_min, T_max)
            ax2.legend(loc="upper right", framealpha=0)

            plt.tight_layout()
            outfile = output_dir.joinpath(f"{chipname}_VI.png")
            log.info(f" Saving {outfile}")
            plt.savefig(outfile)
            plt.close()

            ax1.cla()
            ax2.cla()

            # Internal currents visualization
            fig, ax1 = plt.subplots()
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["IinA"]["Values"],
                marker="o",
                markersize=4,
                label="IinA",
                color="tab:red",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["IinD"]["Values"],
                marker="o",
                markersize=4,
                label="IinD",
                color="tab:red",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["IshuntA"]["Values"],
                marker="o",
                markersize=4,
                label="IshuntA",
                color="tab:blue",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["IshuntD"]["Values"],
                marker="o",
                markersize=4,
                label="IshuntD",
                color="tab:blue",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["IcoreA"]["Values"],
                marker="o",
                markersize=4,
                label="IcoreA",
                color="tab:orange",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["IcoreD"]["Values"],
                marker="o",
                markersize=4,
                label="IcoreD",
                color="tab:orange",
                linestyle="--",
            )
            ax1.plot(
                calculated_data["Current"]["Values"],
                calculated_data["Iref"]["Values"] * 100000,
                marker="o",
                markersize=4,
                label="Iref*100k",
                color="tab:cyan",
            )
            ax1.set_xlabel("I [A]")
            ax1.set_ylabel("I [A]")
            plt.title(f"Currents for chip: {chipname}")

            plt.xlim(I_min, I_max)
            plt.ylim(0.0, Iint_max)
            ax1.legend(loc="upper left", framealpha=0)
            plt.grid()

            ax2 = ax1.twinx()
            ax2.plot(
                calculated_data["Current"]["Values"],
                calculated_data["Temperature"]["Values"],
                marker="^",
                markersize=4,
                color="tab:green",
                label="Temperature (NTC)",
                linestyle="-.",
            )
            ax2.set_ylabel("T [C]")
            ax2.set_ylim(T_min, T_max)
            ax2.legend(loc="upper right", framealpha=0)

            plt.tight_layout()
            outfile = output_dir.joinpath(f"{chipname}_II.png")
            log.info(f" Saving {outfile}")
            plt.savefig(outfile)
            plt.close()

            ax1.cla()
            ax2.cla()

            # SLDO fit
            VinAvg = (
                calculated_data["VinA"]["Values"] + calculated_data["VinD"]["Values"]
            ) / 2.0
            if fit_method.value == "root":
                slope, offset = linear_fit(calculated_data["Current"]["Values"], VinAvg)
            else:
                slope, offset = linear_fit_np(
                    calculated_data["Current"]["Values"], VinAvg
                )

            # Residual analysis
            residual_VinA = (
                p1(calculated_data["Current"]["Values"])
                - (
                    calculated_data["VinA"]["Values"]
                    - calculated_data["Vofs"]["Values"]
                )
            ) * 1000
            residual_VinD = (
                p1(calculated_data["Current"]["Values"])
                - (
                    calculated_data["VinD"]["Values"]
                    - calculated_data["Vofs"]["Values"]
                )
            ) * 1000
            residual_VinA_VinD = (
                calculated_data["VinA"]["Values"] - calculated_data["VinD"]["Values"]
            )
            residual_VinA_nomVofs = (
                p(calculated_data["Current"]["Values"])
                - calculated_data["VinA"]["Values"]
            ) * 1000
            residual_VinD_nomVofs = (
                p(calculated_data["Current"]["Values"])
                - calculated_data["VinD"]["Values"]
            ) * 1000
            residual_Vin = p1(calculated_data["Current"]["Values"]) - (
                VinAvg - calculated_data["Vofs"]["Values"]
            )
            residual_Vofs = (Vofs - calculated_data["Vofs"]["Values"]) * 1000
            res_max = (
                max(
                    max(residual_VinA_nomVofs),
                    max(residual_VinD_nomVofs),
                    max(residual_VinA),
                    max(residual_VinD),
                    max(residual_Vofs),
                )
                + 20
            )
            res_min = (
                min(
                    min(residual_VinA_nomVofs),
                    min(residual_VinD_nomVofs),
                    min(residual_VinA),
                    min(residual_VinD),
                    min(residual_Vofs),
                )
                - 10
            )

            plt.plot(
                calculated_data["Current"]["Values"],
                residual_VinA_nomVofs,
                marker="o",
                markersize=4,
                label=f"{R_eff:.3f}I+{Vofs:.2f}-VinA",
                color="tab:red",
            )
            plt.plot(
                calculated_data["Current"]["Values"],
                residual_VinD_nomVofs,
                marker="o",
                markersize=4,
                label=f"{R_eff:.3f}I+{Vofs:.2f}-VinD",
                color="tab:red",
                linestyle="--",
            )
            plt.plot(
                calculated_data["Current"]["Values"],
                residual_VinA,
                marker="o",
                markersize=4,
                label=f"{R_eff:.3f}I+Vofs-VinA",
                color="tab:blue",
            )
            plt.plot(
                calculated_data["Current"]["Values"],
                residual_VinD,
                marker="o",
                markersize=4,
                label=f"{R_eff:.3f}I+Vofs-VinD",
                color="tab:blue",
                linestyle="--",
            )
            plt.plot(
                calculated_data["Current"]["Values"],
                residual_Vofs,
                marker="o",
                markersize=4,
                label=f"{Vofs}-Vofs",
                color="tab:orange",
            )
            plt.xlabel("I [A]")
            plt.ylabel("V [mV]")
            plt.title(f"VI curve for chip: {chipname}")
            plt.xlim(I_min, I_max)
            plt.ylim(res_min, res_max)
            plt.legend(loc="upper right", framealpha=0)
            plt.grid()
            plt.tight_layout()
            outfile = output_dir.joinpath(f"{chipname}_VIresidual.png")
            log.info(f" Saving {outfile}")
            plt.savefig(outfile)
            plt.close()

            # Find point measured closest to nominal input current
            sldo_nom_input_current = get_nominal_current(layer, nChips)
            log.debug(f" Calculated nominal current to be: {sldo_nom_input_current}")
            idx = (
                np.abs(calculated_data["Current"]["Values"] - sldo_nom_input_current)
            ).argmin()
            log.debug(
                f' Closest current measured to nominal is: {calculated_data["Current"]["Values"][idx]}'
            )

            # Calculate values for QC analysis and output file
            SLDO_LINEARITY = max(residual_Vin, key=lambda x: abs(x))
            SLDO_VINA_VIND = max(residual_VinA_VinD, key=lambda x: abs(x))
            SLDO_VDDA = calculated_data["VDDA"]["Values"][idx]
            SLDO_VDDD = calculated_data["VDDD"]["Values"][idx]
            SLDO_VINA = calculated_data["VinA"]["Values"][idx]
            SLDO_VIND = calculated_data["VinD"]["Values"][idx]
            SLDO_VOFFS = calculated_data["Vofs"]["Values"][idx]
            SLDO_IINA = calculated_data["IinA"]["Values"][idx]
            SLDO_IIND = calculated_data["IinD"]["Values"][idx]
            SLDO_IREF = calculated_data["Iref"]["Values"][idx] * 1e6
            SLDO_ISHUNTA = calculated_data["IshuntA"]["Values"][idx]
            SLDO_ISHUNTD = calculated_data["IshuntD"]["Values"][idx]

            # Load values to dictionary for QC analysis
            results = {}
            results.update({"SLDO_LINEARITY": SLDO_LINEARITY})
            results.update({"SLDO_VINA_VIND": SLDO_VINA_VIND})
            results.update({"SLDO_VDDA": SLDO_VDDA})
            results.update({"SLDO_VDDD": SLDO_VDDD})
            results.update({"SLDO_VINA": SLDO_VINA})
            results.update({"SLDO_VIND": SLDO_VIND})
            results.update({"SLDO_VOFFS": SLDO_VOFFS})
            results.update({"SLDO_IINA": SLDO_IINA})
            results.update({"SLDO_IIND": SLDO_IIND})
            results.update({"SLDO_IREF": SLDO_IREF})
            results.update({"SLDO_ISHUNTA": SLDO_ISHUNTA})
            results.update({"SLDO_ISHUNTD": SLDO_ISHUNTD})

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

            """ Output a json file """
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

            # Calculate additional values for output file only
            analog_overhead = calculated_data["IshuntA"]["Values"][idx] / (
                calculated_data["IinA"]["Values"][idx]
                - calculated_data["IshuntA"]["Values"][idx]
            )
            digital_overhead = calculated_data["IshuntD"]["Values"][idx] / (
                calculated_data["IinD"]["Values"][idx]
                - calculated_data["IshuntD"]["Values"][idx]
            )
            data.add_parameter("SLDO_ANALOG_OVERHEAD", analog_overhead, 3)
            data.add_parameter("SLDO_DIGITAL_OVERHEAD", digital_overhead, 3)
            data.add_parameter("SLDO_VI_SLOPE", slope, 3)
            data.add_parameter("SLDO_VI_OFFSET", offset, 3)
            data.add_parameter("SLDO_NOM_INPUT_CURRENT", sldo_nom_input_current, 3)

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
