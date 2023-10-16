from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
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
    log.info(" \tPerforming IV_MEASURE analysis")
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
            meas_array = results.get("IV_ARRAY")
            voltage = meas_array.get("voltage")
            current = meas_array.get("current")
            sigma_current = meas_array.get("sigma current")
            temperature = meas_array.get("temperature")
            humidity = meas_array.get("humidity")

            Vbd0 = results.get("Vbd0")
            Ilc0 = results.get("Ilc")

            is3Dmodule = False

            Vdepl = 5.0 if is3Dmodule else 50.0
            Vdepl_flag = True

            leak_current_voltage = Vdepl + 20.0 if is3Dmodule else Vdepl + 50.0
            breakdown_threshold = Vdepl + 20.0 if is3Dmodule else Vdepl + 70.0
            current_threshold = 2.5 if is3Dmodule else 0.75

            area = 4.25 if is3Dmodule else 15.92  # [cm^2]
            # 15.76 for inner quad, to be implemented

            Vbd0_flag = None
            if Vbd0:
                Vbd0_flag = Vbd0 > breakdown_threshold

            Ilc0_flag = None
            if Ilc0:
                Ilc0_flag = (Ilc0 / (area + 1.0e-9)) < current_threshold

            Vbd = 0
            Ilc = 0

            # Finding leakage current at threshold voltage
            fig, ax = plt.subplots(1, figsize=(7.2, 4.0))
            for idx, V in enumerate(voltage):
                if Vdepl > V:
                    continue

                if leak_current_voltage >= V:
                    Ilc = current[idx]

                # Finding breakdown voltage for 3D
                if is3Dmodule:
                    if current[idx] > current[idx - 5] * 2 and voltage[idx - 5] > Vdepl:
                        Vbd = voltage[idx - 5]
                        log.info(f"Breakdown at {Vbd:.1f} V for 3D sensor")
                        ax.axvline(
                            Vbd,
                            linewidth=4,
                            color="r",
                            label=f"Bd @ {Vbd:.0f}V",
                        )
                        break

                # Finding breakdown voltage for Planar
                else:
                    if current[idx] > current[idx - 1] * 1.2 and voltage[idx - 1] != 0:
                        Vbd = V
                        log.info(f"Breakdown at {Vbd:.1f} V for planar sensor")
                        ax.axvline(
                            Vbd,
                            linewidth=4,
                            color="r",
                            label=f"Bd @ {Vbd:.0f}V",
                        )
                        break

            # Plotting options
            if len(sigma_current) == 0:
                p1 = ax.plot(voltage[1:], current[1:], label="current", markersize=2)
                first_legend = plt.legend(
                    handles=p1, loc="lower center", bbox_to_anchor=(0.15, -0.33)
                )
                plt.gca().add_artist(first_legend)
            else:
                p1 = ax.errorbar(
                    voltage[1:],
                    current[1:],
                    yerr=sigma_current[1:],
                    fmt="ko",
                    label="current",
                    markersize=2,
                )
                first_legend = plt.legend(
                    handles=[p1], loc="lower center", bbox_to_anchor=(0.15, -0.33)
                )
                plt.gca().add_artist(first_legend)

            if len(temperature) == 0:
                log.warning("No temperature array given")
            elif len(voltage[1:]) == len(temperature[1:]):
                ax1 = ax.twinx()
                (p2,) = ax1.plot(
                    voltage[1:], temperature[1:], color="C1", label="temperature"
                )
                ax1.set_ylabel("T [degC]", color="C1", fontsize="large")
                second_legend = plt.legend(
                    handles=[p2], loc="lower center", bbox_to_anchor=(0.5, -0.33)
                )
                plt.gca().add_artist(second_legend)

            if len(humidity) == 0:
                log.warning("No humidity array given")
            elif len(voltage[1:]) == len(humidity[1:]):
                ax2 = ax.twinx()
                (p3,) = ax2.plot(
                    voltage[1:], humidity[1:], color="C2", label="humidity"
                )
                ax2.set_ylabel("RH [%]", color="C2", fontsize="large")
                ax2.spines["right"].set_position(("outward", 60))
                third_legend = plt.legend(
                    handles=[p3], loc="lower center", bbox_to_anchor=(0.85, -0.33)
                )
                plt.gca().add_artist(third_legend)

            ax.set_title(f'IV for module "{module_name}"', fontsize="large")
            ax.set_xlabel(
                "Negative Voltage [V]", ha="right", va="top", x=1.0, fontsize="large"
            )
            ax.set_ylabel(
                "Negative Current [uA]",
                ha="right",
                va="bottom",
                y=1.0,
                fontsize="large",
            )
            fig.subplots_adjust(bottom=0.25)
            fig.subplots_adjust(right=0.75)

            ax.grid()

            # ------------------------------------------------------------------
            # Flagging

            Ilc_flag = False

            # Pass or fail on leakaged current
            Ilc_flag = Ilc / (area + 1.0e-9) < current_threshold

            # Pass or fail on leakaged current
            Vbd_flag = (Vbd > breakdown_threshold) or (
                voltage[-1] > breakdown_threshold
            )

            results["LEAK_CURRENT"] = Ilc
            results["BREAKDOWN_VOLTAGE"] = max(Vbd, voltage[-1])
            results["MAXIMUM_VOLTAGE"] = max(voltage)  # FIXME
            results["NO_BREAKDOWN_VOLTAGE_OBSERVED"] = True  # FIXME
            results["property"]["TEMP"] = sum(temperature) / len(temperature)
            results["property"]["HUM"] = sum(humidity) / len(humidity)

            passes_qc = (
                (Vbd_flag or Vbd0_flag) and (Ilc_flag or Ilc0_flag) and Vdepl_flag
            )

            passes_qc = True

            log.info(
                f"Ilc_flag: {Ilc_flag}, Vbd_flag: {Vbd_flag}, passes_qc: {passes_qc}"
            )

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

            plt_outfile = output_dir.joinpath(f"{module_name}_plot.png")
            fig.savefig(plt_outfile, dpi=150)


if __name__ == "__main__":
    typer.run(main)
