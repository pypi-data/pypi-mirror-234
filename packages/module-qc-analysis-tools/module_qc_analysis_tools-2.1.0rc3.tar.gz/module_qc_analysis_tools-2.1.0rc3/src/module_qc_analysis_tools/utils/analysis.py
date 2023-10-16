#!/usr/bin/env python3
from __future__ import annotations

import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from module_qc_analysis_tools.utils.misc import (
    bcolors,
    getImuxMap,
    getVmuxMap,
)

log = logging.getLogger("analysis")


def format_text():
    return " {:^30}: {:^20}: {:^20}: {:^5}"


def format_text_short():
    return " {:^30}: {:^20}:"


def print_output_pass(key, results, lower_bound, upper_bound):
    txt = format_text()
    log.info(
        bcolors.OKGREEN
        + txt.format(
            key,
            results,
            f"[{lower_bound}, {upper_bound}]",
            "PASS",
        )
        + bcolors.ENDC
    )


def print_output_fail(key, results, lower_bound, upper_bound):
    txt = format_text()
    log.info(
        bcolors.BADRED
        + txt.format(
            key,
            results,
            f"[{lower_bound}, {upper_bound}]",
            "FAIL",
        )
        + bcolors.ENDC
    )


def print_output_neutral(key, results):
    txt = format_text_short()
    log.info(bcolors.WARNING + txt.format(key, round(results, 2)) + bcolors.ENDC)


def get_layer(layer):
    layers = {"L0": "LZero", "L1": "LOne", "L2": "LTwo"}
    return layers.get(layer)


def check_layer(layer):
    possible_layers = ["L0", "L1", "L2"]
    if layer not in possible_layers:
        log.error(
            bcolors.ERROR
            + f" Layer '{layer}' not recognized or not provided. Provide the layer with the --layer [L0, L1, or L2] option."
            + bcolors.ENDC
        )
        sys.exit(-1)


def get_n_chips(layer):
    check_layer(layer)
    chips_per_layer = {"L0": 3, "L1": 4, "L2": 4}
    return chips_per_layer.get(layer)


# The following hardcoded values are from https://gitlab.cern.ch/atlas-itk/pixel/module/itkpix-electrical-qc
def get_nominal_current(layer, nchips):
    check_layer(layer)
    # Assumes triplets for L0, quads for L1-L2
    currents_per_chip = {
        "L0": 1.85,
        "L1": 1.65,
        "L2": 1.47,
    }
    return currents_per_chip.get(layer) * nchips


def get_nominal_Voffs(layer, lp_mode=False):
    check_layer(layer)
    Voffs = {
        "L0": 1.1,
        "L1": 1.0,
        "L2": 1.0,
    }
    Voffs_lp = {
        "L0": 1.38,
        "L1": 1.38,
        "L2": 1.38,
    }
    if lp_mode:
        return Voffs_lp.get(layer)

    return Voffs.get(layer)


def get_nominal_RextA(layer):
    check_layer(layer)
    RextA = {
        "L0": 511,
        "L1": 732,
        "L2": 866,
    }
    return RextA.get(layer)


def get_nominal_RextD(layer):
    check_layer(layer)
    RextD = {"L0": 407, "L1": 549, "L2": 590}
    return RextD.get(layer)


# Function to get key from value in muxMaps
def get_key(mydict, val):
    for key, value in mydict.items():
        if val == value:
            return key
    return -1


def perform_qc_analysis_AR_NOMINAL_SETTINGS(_test_type, qc_config, layer, results):
    # QC analysis for AR_NOMINAL_SETTINGS

    rounded_results_list = results.copy()
    cell_text = np.empty(0)
    passes_qc_overall = True
    VmuxMap = getVmuxMap()
    ImuxMap = getImuxMap()
    max_precision = 0
    if len(VmuxMap.keys()) + len(ImuxMap.keys()) != len(results):
        log.error(
            bcolors.ERROR
            + " Number of entries in AR_NOMINAL_SETTINGS results does not match number of entries in VmuxMap and ImuxMap - there should be one entry for every Vmux and Imux in those maps. Please fix and re-run!"
            + bcolors.ENDC
        )
        return -1
    for key, value in qc_config.items():
        log.debug(f" QC selections for {key}: {value}")
        if value.get("sel"):
            try:
                lower_bound = value.get("sel")[0]
                upper_bound = value.get("sel")[1]
                precision = value.get("precision")
            except Exception:
                log.error(
                    bcolors.ERROR
                    + f" QC selections for {key} are ill-formatted, should be list of length 2! Please fix: {value} . Skipping."
                    + bcolors.ENDC
                )
                continue
        elif value.get("LZero"):
            try:
                layer_bounds = value.get(layer).get("sel")
            except Exception:
                log.error(
                    bcolors.ERROR
                    + f" QC selections for {key} and {layer} do not exist - please check! Skipping."
                    + bcolors.ENDC
                )
                continue
            lower_bound = layer_bounds[0]
            upper_bound = layer_bounds[1]
            precision = value.get(layer).get("precision")

        passes_qc_test = True
        if get_key(ImuxMap, key) != -1:
            index = get_key(ImuxMap, key)
        elif get_key(VmuxMap, key) != -1:
            index = get_key(VmuxMap, key) + len(ImuxMap.keys())
        else:
            log.error(
                bcolors.ERROR
                + f"Did not find {key} in VmuxMap or ImuxMap - please check!"
                + bcolors.ENDC
            )
            continue
        log.debug(f" Key is {key}, value is {value}, index is {index}")

        if results[index] == -999:
            log.error(
                bcolors.ERROR
                + f" Parameter from chip for QC selection of {key} was not passed to analysis - please fix!"
                + bcolors.ENDC
            )
            passes_qc_test = False

        if precision > max_precision:
            max_precision = precision
        rounded_results = round(results[index], precision)
        rounded_results_list[index] = rounded_results
        if (rounded_results < lower_bound) or (rounded_results > upper_bound):
            passes_qc_test = False
        if passes_qc_test:
            print_output_pass(key, rounded_results, lower_bound, upper_bound)
        else:
            print_output_fail(key, rounded_results, lower_bound, upper_bound)

        cell_text = np.append(
            cell_text,
            [
                key,
                rounded_results,
                f"[{lower_bound}, {upper_bound}]",
                passes_qc_test,
            ],
        )

        passes_qc_overall = passes_qc_overall and passes_qc_test

    # Round all value not used in QC to default value (max precision from any value)
    rounded_results_list = [round(elem, max_precision) for elem in rounded_results_list]

    return passes_qc_overall, cell_text, rounded_results_list


def perform_qc_analysis_AR_VDD_Trim(_test_type, qc_config, _layer, results, key):
    # QC analysis for VDDA_VS_TRIM and VDDD_VS_TRIM
    pass_vdd_vs_trim_test = True

    cell_text = np.empty(0)
    # Check that nominal VDD value is between 2nd and 13th trim value
    for trim in [2, 13]:
        tmp_pass_qc = True

        lower_bound_vdd = qc_config.get(f"VDD_TRIM_{trim}").get("sel")[0]
        upper_bound_vdd = qc_config.get(f"VDD_TRIM_{trim}").get("sel")[1]

        precision = qc_config.get(f"VDD_TRIM_{trim}").get("precision")
        rounded_results = round(results[trim], precision)

        if (rounded_results < lower_bound_vdd) or (rounded_results > upper_bound_vdd):
            tmp_pass_qc = False
        if tmp_pass_qc:
            print_output_pass(
                f"{key}_{trim}", rounded_results, lower_bound_vdd, upper_bound_vdd
            )
        else:
            print_output_fail(
                f"{key}_{trim}", rounded_results, lower_bound_vdd, upper_bound_vdd
            )
        cell_text = np.append(
            cell_text,
            [
                f"{key}_{trim}",
                rounded_results,
                f"[{lower_bound_vdd}, {upper_bound_vdd}]",
                tmp_pass_qc,
            ],
        )
        pass_vdd_vs_trim_test = pass_vdd_vs_trim_test and tmp_pass_qc

    # The trim step size (change in voltage per DAC step) must satisfy requirements
    VDD_dV_list = np.diff(np.array(results))
    lower_bound_dv = qc_config.get("VDD_step_size").get("sel")[0]
    upper_bound_dv = qc_config.get("VDD_step_size").get("sel")[1]
    precision = qc_config.get("VDD_step_size").get("precision")

    rounded_results = np.around(VDD_dV_list, precision)
    dV_fail = (rounded_results < lower_bound_dv) | (rounded_results > upper_bound_dv)
    pass_vdd_vs_trim_test = pass_vdd_vs_trim_test and bool(np.any(dV_fail))
    for i in range(len(rounded_results)):
        tmp_pass_qc = not dV_fail[i]
        if tmp_pass_qc:
            print_output_pass(
                f"{key}_{i+1}_STEP_SIZE",
                rounded_results[i],
                lower_bound_dv,
                upper_bound_dv,
            )
        else:
            print_output_fail(
                f"{key}_{i+1}_STEP_SIZE",
                rounded_results[i],
                lower_bound_dv,
                upper_bound_dv,
            )
        cell_text = np.append(
            cell_text,
            [
                f"{key}_{i+1}_STEP_SIZE",
                rounded_results[i],
                f"[{lower_bound_dv}, {upper_bound_dv}]",
                tmp_pass_qc,
            ],
        )

    # Round all VDD values to same precision
    rounded_results_list = [
        round(
            elem,
            max(
                qc_config.get("VDD_step_size").get("precision"),
                qc_config.get("VDD_TRIM_2").get("precision"),
            ),
        )
        for elem in results
    ]

    return pass_vdd_vs_trim_test, cell_text, rounded_results_list


def perform_qc_analysis_AR_ROSC(_test_type, qc_config, _layer, results, key):
    # QC analysis for ROSC_VS_VDDD
    pass_rosc_vs_vddd_test = True

    rounded_results_list = results.copy()
    cell_text = np.empty(0)

    for i in range(len(results)):
        tmp_pass_qc = True
        lower_bound = (
            qc_config.get("sel")[0]
            if "RESIDUAL" in key
            else qc_config.get(f"ROSC{i}").get("sel")[0]
        )
        upper_bound = (
            qc_config.get("sel")[1]
            if "RESIDUAL" in key
            else qc_config.get(f"ROSC{i}").get("sel")[1]
        )
        precision = (
            qc_config.get("precision")
            if "RESIDUAL" in key
            else qc_config.get(f"ROSC{i}").get("precision")
        )
        rounded_results = round(results[i], precision)
        rounded_results_list[i] = rounded_results

        if (rounded_results < lower_bound) or (rounded_results > upper_bound):
            tmp_pass_qc = False
        if tmp_pass_qc:
            print_output_pass(f"{key}_{i}", rounded_results, lower_bound, upper_bound)
        else:
            print_output_fail(f"{key}_{i}", rounded_results, lower_bound, upper_bound)
        cell_text = np.append(
            cell_text,
            [
                f"{key}_{i}",
                rounded_results,
                f"[{lower_bound}, {upper_bound}]",
                tmp_pass_qc,
            ],
        )
        pass_rosc_vs_vddd_test = pass_rosc_vs_vddd_test and tmp_pass_qc

    return pass_rosc_vs_vddd_test, cell_text, rounded_results_list


# Function takes as input test type (i.e. ADC_CALIBRATION), file containing QC selections,
# and dictionary with results. Returns QC result (true/false), a numpy array of text to
# be printed later into a table, and the same result dictionary it was passed, but with
# the values rounded to the same precision as the QC selection they are compared to.
def perform_qc_analysis(test_type, qc_selections, layer_name, results):
    log.info("")
    log.info("Performing QC analysis!")
    log.info("")

    check_qc_selections = qc_selections.copy()

    check_layer(layer_name)
    layer = get_layer(layer_name)

    passes_qc_overall = True
    txt = format_text()
    log.info(txt.format("Parameter", "Analysis result", "QC criteria", "Pass"))
    log.info(
        "--------------------------------------------------------------------------------------"
    )

    # Setup arrays for plotting
    cell_text = np.empty(0)

    # Setup rounded result dictionary
    rounded_results_dict = results.copy()

    for key in results:
        if not qc_selections.get(key):
            log.debug(
                bcolors.WARNING
                + f" Selection for {key} not found in QC file! Skipping."
                + bcolors.ENDC
            )
            print_output_neutral(key, results.get(key))
            continue
        check_qc_selections.pop(key)

        # Handle AR_NOMINAL_SETTINGS in completely different function, for now...
        if key == "AR_NOMINAL_SETTINGS":
            (
                passes_qc_test,
                new_cell_text,
                rounded_list,
            ) = perform_qc_analysis_AR_NOMINAL_SETTINGS(
                test_type,
                qc_selections.get(key),
                layer,
                results.get(key),
            )
            rounded_results_dict.update({key: rounded_list})
            cell_text = np.append(cell_text, new_cell_text)
            passes_qc_overall = passes_qc_overall and passes_qc_test
            continue

        # Handle AR_VDDA_VS_TRIM and AR_VDD_VS_TRIM separately
        if ("AR_VDDA_VS_TRIM" in key) or ("AR_VDDD_VS_TRIM" in key):
            (
                passes_qc_test,
                new_cell_text,
                rounded_list,
            ) = perform_qc_analysis_AR_VDD_Trim(
                test_type,
                qc_selections.get(key),
                layer,
                results.get(key),
                key,
            )
            rounded_results_dict.update({key: rounded_list})
            cell_text = np.append(cell_text, new_cell_text)
            passes_qc_overall = passes_qc_overall and passes_qc_test
            continue

        # Handle AR_ROSC_SLOPE and AR_ROSC_OFFSET separately
        if "AR_ROSC" in key:
            passes_qc_test, new_cell_text, rounded_list = perform_qc_analysis_AR_ROSC(
                test_type,
                qc_selections.get(key),
                layer,
                results.get(key),
                key,
            )
            rounded_results_dict.update({key: rounded_list})
            cell_text = np.append(cell_text, new_cell_text)
            passes_qc_overall = passes_qc_overall and passes_qc_test
            continue

        log.debug(f" QC selections for {key}: {qc_selections.get(key).get('sel')}")
        if type(qc_selections.get(key).get("sel")) is list:
            if len(qc_selections.get(key).get("sel")) != 2:
                log.error(
                    bcolors.ERROR
                    + f" QC selections for {key} are ill-formatted, should be list of length 2! Please fix: {qc_selections.get(key).get('sel')} . Skipping."
                    + bcolors.ENDC
                )
                continue
            lower_bound = qc_selections.get(key).get("sel")[0]
            upper_bound = qc_selections.get(key).get("sel")[1]
            precision = qc_selections.get(key).get("precision")
        elif qc_selections.get(key).get("LZero"):
            layer_bounds = qc_selections.get(key).get(layer).get("sel")
            if not layer_bounds:
                log.error(
                    bcolors.ERROR
                    + f" QC selections for {key} and {layer} do not exist - please check! Skipping."
                    + bcolors.ENDC
                )
                continue
            lower_bound = layer_bounds[0]
            upper_bound = layer_bounds[1]
            precision = qc_selections.get(key).get(layer).get("precision")

        rounded_results = round(results.get(key), precision)
        rounded_results_dict.update({key: rounded_results})
        passes_qc_test = True
        if rounded_results < lower_bound or rounded_results > upper_bound:
            passes_qc_test = False
        if passes_qc_test:
            print_output_pass(key, rounded_results, lower_bound, upper_bound)
        else:
            print_output_fail(key, rounded_results, lower_bound, upper_bound)
        passes_qc_overall = passes_qc_overall and passes_qc_test

        cell_text = np.append(
            cell_text,
            [
                key,
                rounded_results,
                f"[{lower_bound}, {upper_bound}]",
                passes_qc_test,
            ],
        )
    if len(check_qc_selections) > 0:
        for key in check_qc_selections:
            log.error(
                bcolors.ERROR
                + f" Parameter from chip for QC selection of {key} was not passed to analysis - please fix!"
                + bcolors.ENDC
            )
        passes_qc_overall = False
    log.info(
        "--------------------------------------------------------------------------------------"
    )

    return passes_qc_overall, cell_text, rounded_results_dict


def print_result_summary(cell_text, test_type, outputdir, chipname, label=""):
    # Turn off matplotlib DEBUG messages
    plt.set_loglevel(level="warning")

    cell_text = cell_text.reshape(-1, 4)
    nrows, ncols = cell_text.shape
    cellColours = np.empty(0)
    for r in range(0, nrows):
        if cell_text[r][3] == "True":
            cellColours = np.append(cellColours, ["lightgreen"] * 4)
        else:
            cellColours = np.append(cellColours, ["lightcoral"] * 4)
    cellColours = cellColours.reshape(-1, 4)
    colLabels = np.array(["Parameter", "Analysis result", "QC criteria", "Pass"])
    colWidths = [1.2, 0.4, 0.5, 0.3]

    if test_type == "ANALOG_READBACK":
        cell_text1 = cell_text[0:33, :]
        cellColours1 = cellColours[:33, :]
        nrows, ncols = cell_text1.shape
        fig, ax = plt.subplots(figsize=(6.4, 1.5 + nrows * 0.5))
        table = ax.table(
            cellText=cell_text1,
            colLabels=colLabels,
            loc="upper center",
            cellLoc="center",
            colWidths=colWidths,
            cellColours=cellColours1,
        )
        format_result_summary(
            fig, ax, table, chipname, test_type, outputdir, f"{label}1"
        )

        cell_text2 = cell_text[33:65, :]
        cellColours2 = cellColours[33:65, :]
        nrows, ncols = cell_text2.shape
        fig, ax = plt.subplots(figsize=(6.4, 1.5 + nrows * 0.5))
        table = ax.table(
            cellText=cell_text2,
            colLabels=colLabels,
            loc="upper center",
            cellLoc="center",
            colWidths=colWidths,
            cellColours=cellColours2,
        )
        format_result_summary(
            fig, ax, table, chipname, test_type, outputdir, f"{label}2"
        )

        cell_text3 = cell_text[65:107, :]
        cellColours3 = cellColours[65:107, :]
        nrows, ncols = cell_text3.shape
        fig, ax = plt.subplots(figsize=(6.4, 1.5 + nrows * 0.5))
        table = ax.table(
            cellText=cell_text3,
            colLabels=colLabels,
            loc="upper center",
            cellLoc="center",
            colWidths=colWidths,
            cellColours=cellColours3,
        )
        format_result_summary(
            fig, ax, table, chipname, test_type, outputdir, f"{label}3"
        )

        cell_text4 = cell_text[107:149, :]
        cellColours4 = cellColours[107:149, :]
        nrows, ncols = cell_text4.shape
        fig, ax = plt.subplots(figsize=(6.4, 1.5 + nrows * 0.5))
        table = ax.table(
            cellText=cell_text4,
            colLabels=colLabels,
            loc="upper center",
            cellLoc="center",
            colWidths=colWidths,
            cellColours=cellColours4,
        )
        format_result_summary(
            fig, ax, table, chipname, test_type, outputdir, f"{label}4"
        )

        cell_text5 = cell_text[149:191, :]
        cellColours5 = cellColours[149:191, :]
        nrows, ncols = cell_text3.shape
        fig, ax = plt.subplots(figsize=(6.4, 1.5 + nrows * 0.5))
        table = ax.table(
            cellText=cell_text5,
            colLabels=colLabels,
            loc="upper center",
            cellLoc="center",
            colWidths=colWidths,
            cellColours=cellColours5,
        )
        format_result_summary(
            fig, ax, table, chipname, test_type, outputdir, f"{label}5"
        )

    else:
        fig, ax = plt.subplots(figsize=(6.4, 1.5 + nrows * 0.5))
        table = ax.table(
            cellText=cell_text,
            colLabels=colLabels,
            loc="upper center",
            cellLoc="center",
            colWidths=colWidths,
            cellColours=cellColours,
        )
        format_result_summary(fig, ax, table, chipname, test_type, outputdir, label)


def format_result_summary(fig, ax, table, chipname, test_type, outputdir, label=""):
    fig.patch.set_visible(False)
    if label is not None:
        label = f"_{label}"
    ax.axis("off")
    ax.axis("tight")
    table.scale(1, 3)
    ax.set_title(f"{test_type} for {chipname}", fontsize=15)
    table.auto_set_font_size(False)
    table.set_fontsize(15)
    plt.savefig(
        outputdir.joinpath(f"{chipname}_summary{label}.png"),
        bbox_inches="tight",
        dpi=100,
        transparent=False,
        edgecolor="white",
    )
    log.info("Saving " + str(outputdir.joinpath(f"{chipname}_summary{label}.png")))
    plt.close()


def submit_results(
    outputDF, timestamp, site="Unspecified", outputfile="submit.txt", layer="Unknown"
):
    results = outputDF.get("results")

    # Temporary solution to avoid error when indexing array that doesn't exist
    if not results.get("AR_VDDA_VS_TRIM"):
        results.update({"AR_VDDA_VS_TRIM": [-1] * 16})
    if not results.get("AR_VDDD_VS_TRIM"):
        results.update({"AR_VDDD_VS_TRIM": [-1] * 16})
    if not results.get("AR_ROSC_SLOPE"):
        results.update({"AR_ROSC_SLOPE": [-1] * 42})
    if not results.get("AR_ROSC_OFFSET"):
        results.update({"AR_ROSC_OFFSET": [-1] * 42})
    if not results.get("AR_NOMINAL_SETTINGS"):
        results.update({"AR_NOMINAL_SETTINGS": [-1] * 72})
    analysis_version = results.get("property").get("ANALYSIS_VERSION")
    meas_version = results.get("Metadata").get("MEASUREMENT_VERSION")

    url = {
        "ADC_CALIBRATION": f"https://docs.google.com/forms/d/e/1FAIpQLSegDYRQ1Foe5eTuSOVZUXe0d1f_Bh5v3rhsffCnu9DUDFR69A/formResponse?usp=pp_url\
	&entry.1920584355={timestamp}\
	&entry.1282466276={outputDF.get('passed')}\
	&entry.141409196={analysis_version}\
	&entry.1579707472={meas_version}\
	&entry.913205750={layer}\
	&entry.104853658={outputDF.get('serialNumber')}\
	&entry.802167553={site}\
	&entry.1592726943={results.get('ADC_CALIBRATION_SLOPE')}\
	&entry.422835427={results.get('ADC_CALIBRATION_OFFSET')}",
        "VCAL_CALIBRATION": f"https://docs.google.com/forms/d/e/1FAIpQLSenLUdLpaHLssp-jdUf1YvqiWvR8WOAkhrpQgfBlZYTWWRNog/formResponse?usp=pp_url\
	&entry.1920584355={timestamp}\
	&entry.796846737={outputDF.get('passed')}\
	&entry.1436190418={analysis_version}\
	&entry.463035701={meas_version}\
	&entry.74191116={layer}\
	&entry.104853658={outputDF.get('serialNumber')}\
	&entry.802167553={site}\
	&entry.1592726943={results.get('VCAL_MED_SLOPE')}\
	&entry.422835427={results.get('VCAL_MED_OFFSET')}\
	&entry.424316677={results.get('VCAL_MED_SLOPE_SMALL_RANGE')}\
	&entry.2055663117={results.get('VCAL_MED_OFFSET_SMALL_RANGE')}\
	&entry.1630084203={results.get('VCAL_HIGH_SLOPE')}\
	&entry.1107555352={results.get('VCAL_HIGH_OFFSET')}\
	&entry.1994936328={results.get('VCAL_HIGH_SLOPE_SMALL_RANGE')}\
	&entry.524584120={results.get('VCAL_HIGH_OFFSET_SMALL_RANGE')}",
        "INJECTION_CAPACITANCE": f"https://docs.google.com/forms/d/e/1FAIpQLSfHpq9pjuzgYvjUU8ZHapzCOrIHzyJx3xirJunGEtBO2COYGw/formResponse?usp=pp_url\
	&entry.1920584355={timestamp}\
	&entry.346685867={outputDF.get('passed')}\
	&entry.2076657244={analysis_version}\
	&entry.2143111336={meas_version}\
	&entry.1736672890={layer}\
	&entry.104853658={outputDF.get('serialNumber')}\
	&entry.802167553={site}\
	&entry.1714546984={results.get('INJ_CAPACITANCE')}",
        "LP_MODE": f"https://docs.google.com/forms/d/e/1FAIpQLSdVBudYiVFG9ts_0y6bQ4xhGJ-mIJNM-N1Hcs7jgPhiYVNAwA/formResponse?usp=pp_url\
	&entry.1920584355={timestamp}\
	&entry.104853658={outputDF.get('serialNumber')}\
	&entry.1282466276={outputDF.get('passed')}\
	&entry.141409196={analysis_version}\
	&entry.1579707472={meas_version}\
	&entry.913205750={layer}\
	&entry.802167553={site}\
	&entry.1592726943={results.get('LP_VINA')}\
	&entry.422835427={results.get('LP_VIND')}\
	&entry.1218296463={results.get('LP_VOFFS')}\
	&entry.1682731027={results.get('LP_IINA')}\
	&entry.784021623={results.get('LP_IIND')}\
	&entry.1188204940={results.get('LP_ISHUNTA')}\
	&entry.1456818826={results.get('LP_ISHUNTD')}\
	&entry.1355617557={results.get('LP_DIGITAL_FAIL')}",
        "OVERVOLTAGE_PROTECTION": f"https://docs.google.com/forms/d/e/1FAIpQLSc0lwqev5Yyozmnn3gkdnTOoH9BbSdjOuL7CAbhQOZ2rTJINg/formResponse?usp=pp_url\
	&entry.1920584355={timestamp}\
	&entry.104853658={outputDF.get('serialNumber')}\
	&entry.1282466276={outputDF.get('passed')}\
	&entry.141409196={analysis_version}\
	&entry.1579707472={meas_version}\
	&entry.913205750={layer}\
	&entry.802167553={site}\
	&entry.1592726943={results.get('OVP_VINA')}\
	&entry.422835427={results.get('OVP_VIND')}\
	&entry.1218296463={results.get('OVP_VREFOVP')}\
	&entry.1682731027={results.get('OVP_IINA')}\
	&entry.784021623={results.get('OVP_IIND')}",
        "SLDO": f"https://docs.google.com/forms/d/e/1FAIpQLSf3NC84OaYYjJ-DgQ29RvMV2dDQnUI0nxBFdnCUVMby7RXOFQ/formResponse?usp=pp_url\
	&entry.910646842={outputDF.get('serialNumber')}\
	&entry.1225658339={outputDF.get('passed')}\
	&entry.2052956027={analysis_version}\
	&entry.314862968={meas_version}\
	&entry.137143573={layer}\
	&entry.507508481={site}\
	&entry.1425106615={timestamp}\
	&entry.613380586={results.get('SLDO_VI_SLOPE')}\
	&entry.2009791679={results.get('SLDO_VI_OFFSET')}\
	&entry.1877869140={results.get('SLDO_NOM_INPUT_CURRENT')}\
	&entry.1380637801={results.get('SLDO_VDDA')}\
	&entry.959013471={results.get('SLDO_VDDD')}\
	&entry.427742248={results.get('SLDO_VINA')}\
	&entry.1100117192={results.get('SLDO_VIND')}\
	&entry.411324334={results.get('SLDO_VOFFS')}\
	&entry.257023545={results.get('SLDO_IINA')}\
	&entry.172777573={results.get('SLDO_IIND')}\
	&entry.2138863081={results.get('SLDO_IREF')}\
	&entry.1216431295={results.get('SLDO_ISHUNTA')}\
	&entry.825886502={results.get('SLDO_ISHUNTD')}\
	&entry.298426805={results.get('SLDO_ANALOG_OVERHEAD')}\
	&entry.187142037={results.get('SLDO_DIGITAL_OVERHEAD')}\
	&entry.844801892={results.get('SLDO_LINEARITY')}\
	&entry.812048396={results.get('SLDO_VINA_VIND')}",
        "ANALOG_READBACK": f"https://docs.google.com/forms/d/e/1FAIpQLScsfVAnZokYd-CDef1WZGgdNEY-AdqeS3erRF1mzy6Bl37eYg/formResponse?usp=pp_url\
	&entry.910646842={outputDF.get('serialNumber')}\
	&entry.351877676={outputDF.get('passed')}\
	&entry.2065736414={analysis_version}\
	&entry.1608510255={meas_version}\
	&entry.1353243899={layer}\
	&entry.507508481={site}\
	&entry.1425106615={timestamp}\
	&entry.613380586={results.get('AR_NOMINAL_SETTINGS')[0]}\
	&entry.2091108240={results.get('AR_NOMINAL_SETTINGS')[1]}\
	&entry.1308096676={results.get('AR_NOMINAL_SETTINGS')[2]}\
	&entry.1616657488={results.get('AR_NOMINAL_SETTINGS')[3]}\
	&entry.303689355={results.get('AR_NOMINAL_SETTINGS')[4]}\
	&entry.1299197252={results.get('AR_NOMINAL_SETTINGS')[5]}\
	&entry.337124367={results.get('AR_NOMINAL_SETTINGS')[6]}\
	&entry.539725220={results.get('AR_NOMINAL_SETTINGS')[7]}\
	&entry.174520567={results.get('AR_NOMINAL_SETTINGS')[8]}\
	&entry.2077557631={results.get('AR_NOMINAL_SETTINGS')[9]}\
	&entry.1152177529={results.get('AR_NOMINAL_SETTINGS')[10]}\
	&entry.1170074988={results.get('AR_NOMINAL_SETTINGS')[11]}\
	&entry.1695410680={results.get('AR_NOMINAL_SETTINGS')[12]}\
	&entry.1683989630={results.get('AR_NOMINAL_SETTINGS')[13]}\
	&entry.637795568={results.get('AR_NOMINAL_SETTINGS')[14]}\
	&entry.1796334891={results.get('AR_NOMINAL_SETTINGS')[15]}\
	&entry.1192471500={results.get('AR_NOMINAL_SETTINGS')[16]}\
	&entry.1037413000={results.get('AR_NOMINAL_SETTINGS')[17]}\
	&entry.1731827348={results.get('AR_NOMINAL_SETTINGS')[18]}\
	&entry.1788264831={results.get('AR_NOMINAL_SETTINGS')[19]}\
	&entry.1271298835={results.get('AR_NOMINAL_SETTINGS')[20]}\
	&entry.294928269={results.get('AR_NOMINAL_SETTINGS')[21]}\
	&entry.1752002697={results.get('AR_NOMINAL_SETTINGS')[22]}\
	&entry.1789768564={results.get('AR_NOMINAL_SETTINGS')[23]}\
	&entry.19338211={results.get('AR_NOMINAL_SETTINGS')[24]}\
	&entry.1373225730={results.get('AR_NOMINAL_SETTINGS')[25]}\
	&entry.1288561285={results.get('AR_NOMINAL_SETTINGS')[26]}\
	&entry.993587744={results.get('AR_NOMINAL_SETTINGS')[27]}\
	&entry.1225105463={results.get('AR_NOMINAL_SETTINGS')[28]}\
	&entry.2014795413={results.get('AR_NOMINAL_SETTINGS')[29]}\
	&entry.814046228={results.get('AR_NOMINAL_SETTINGS')[30]}\
	&entry.1206599091={results.get('AR_NOMINAL_SETTINGS')[31]}\
	&entry.1046023025={results.get('AR_NOMINAL_SETTINGS')[32]}\
	&entry.125849508={results.get('AR_NOMINAL_SETTINGS')[33]}\
	&entry.278665318={results.get('AR_NOMINAL_SETTINGS')[34]}\
	&entry.1317511634={results.get('AR_NOMINAL_SETTINGS')[35]}\
	&entry.799431715={results.get('AR_NOMINAL_SETTINGS')[36]}\
	&entry.1032356051={results.get('AR_NOMINAL_SETTINGS')[37]}\
	&entry.206739602={results.get('AR_NOMINAL_SETTINGS')[38]}\
	&entry.47441728={results.get('AR_NOMINAL_SETTINGS')[39]}\
	&entry.887166253={results.get('AR_NOMINAL_SETTINGS')[40]}\
	&entry.290527652={results.get('AR_NOMINAL_SETTINGS')[41]}\
	&entry.1481344879={results.get('AR_NOMINAL_SETTINGS')[42]}\
	&entry.155322339={results.get('AR_NOMINAL_SETTINGS')[43]}\
	&entry.556597681={results.get('AR_NOMINAL_SETTINGS')[44]}\
	&entry.1293797041={results.get('AR_NOMINAL_SETTINGS')[45]}\
	&entry.1984481605={results.get('AR_NOMINAL_SETTINGS')[46]}\
	&entry.1633430606={results.get('AR_NOMINAL_SETTINGS')[47]}\
	&entry.1430993123={results.get('AR_NOMINAL_SETTINGS')[48]}\
	&entry.526213623={results.get('AR_NOMINAL_SETTINGS')[49]}\
	&entry.1631275305={results.get('AR_NOMINAL_SETTINGS')[50]}\
	&entry.975590254={results.get('AR_NOMINAL_SETTINGS')[51]}\
	&entry.1474828103={results.get('AR_NOMINAL_SETTINGS')[52]}\
	&entry.1495459865={results.get('AR_NOMINAL_SETTINGS')[53]}\
	&entry.1128496051={results.get('AR_NOMINAL_SETTINGS')[54]}\
	&entry.367477458={results.get('AR_NOMINAL_SETTINGS')[55]}\
	&entry.1466626922={results.get('AR_NOMINAL_SETTINGS')[56]}\
	&entry.631124052={results.get('AR_NOMINAL_SETTINGS')[57]}\
	&entry.946981503={results.get('AR_NOMINAL_SETTINGS')[58]}\
	&entry.571213202={results.get('AR_NOMINAL_SETTINGS')[59]}\
	&entry.688702844={results.get('AR_NOMINAL_SETTINGS')[60]}\
	&entry.431853336={results.get('AR_NOMINAL_SETTINGS')[61]}\
	&entry.1724286670={results.get('AR_NOMINAL_SETTINGS')[62]}\
	&entry.2112361286={results.get('AR_NOMINAL_SETTINGS')[63]}\
	&entry.1689766951={results.get('AR_NOMINAL_SETTINGS')[64]}\
	&entry.2142543004={results.get('AR_NOMINAL_SETTINGS')[65]}\
	&entry.1946421005={results.get('AR_NOMINAL_SETTINGS')[66]}\
	&entry.707341702={results.get('AR_NOMINAL_SETTINGS')[67]}\
	&entry.1328302698={results.get('AR_NOMINAL_SETTINGS')[68]}\
	&entry.1022788500={results.get('AR_NOMINAL_SETTINGS')[69]}\
	&entry.973739200={results.get('AR_NOMINAL_SETTINGS')[70]}\
	&entry.1279705270={results.get('AR_NOMINAL_SETTINGS')[71]}\
	&entry.1637225517={results.get('AR_TEMP_NTC')}\
	&entry.1793217377={results.get('AR_TEMP_EXT')}\
	&entry.2135558015={results.get('AR_TEMP_ASLDO')}\
	&entry.1505388309={results.get('AR_TEMP_DSLDO')}\
	&entry.363112736={results.get('AR_TEMP_ACB')}\
	&entry.1942035528={results.get('AR_TEMP_ACB')}\
	&entry.1251896209={results.get('AR_VDDA_VS_TRIM')[0]}\
	&entry.896618670={results.get('AR_VDDA_VS_TRIM')[1]}\
	&entry.60914654={results.get('AR_VDDA_VS_TRIM')[2]}\
	&entry.961303064={results.get('AR_VDDA_VS_TRIM')[3]}\
	&entry.448329889={results.get('AR_VDDA_VS_TRIM')[4]}\
	&entry.1155979196={results.get('AR_VDDA_VS_TRIM')[5]}\
	&entry.412804010={results.get('AR_VDDA_VS_TRIM')[6]}\
	&entry.949350985={results.get('AR_VDDA_VS_TRIM')[7]}\
	&entry.307370261={results.get('AR_VDDA_VS_TRIM')[8]}\
	&entry.409514081={results.get('AR_VDDA_VS_TRIM')[9]}\
	&entry.2001782359={results.get('AR_VDDA_VS_TRIM')[10]}\
	&entry.10329903={results.get('AR_VDDA_VS_TRIM')[11]}\
	&entry.1636667111={results.get('AR_VDDA_VS_TRIM')[12]}\
	&entry.685698936={results.get('AR_VDDA_VS_TRIM')[13]}\
	&entry.537201174={results.get('AR_VDDA_VS_TRIM')[14]}\
	&entry.1053736177={results.get('AR_VDDA_VS_TRIM')[15]}\
	&entry.1435921809={results.get('AR_VDDD_VS_TRIM')[0]}\
	&entry.1499425666={results.get('AR_VDDD_VS_TRIM')[1]}\
	&entry.1890145904={results.get('AR_VDDD_VS_TRIM')[2]}\
	&entry.383115039={results.get('AR_VDDD_VS_TRIM')[3]}\
	&entry.398663489={results.get('AR_VDDD_VS_TRIM')[4]}\
	&entry.1566918433={results.get('AR_VDDD_VS_TRIM')[5]}\
	&entry.1555345873={results.get('AR_VDDD_VS_TRIM')[6]}\
	&entry.1092876262={results.get('AR_VDDD_VS_TRIM')[7]}\
	&entry.1293594936={results.get('AR_VDDD_VS_TRIM')[8]}\
	&entry.2099215210={results.get('AR_VDDD_VS_TRIM')[9]}\
	&entry.413539179={results.get('AR_VDDD_VS_TRIM')[10]}\
	&entry.1080321692={results.get('AR_VDDD_VS_TRIM')[11]}\
	&entry.259801418={results.get('AR_VDDD_VS_TRIM')[12]}\
	&entry.2100743637={results.get('AR_VDDD_VS_TRIM')[13]}\
	&entry.1600042255={results.get('AR_VDDD_VS_TRIM')[14]}\
	&entry.50695564={results.get('AR_VDDD_VS_TRIM')[15]}\
	&entry.1267721453={results.get('AR_ROSC_SLOPE')[0]}\
	&entry.1108238171={results.get('AR_ROSC_SLOPE')[1]}\
	&entry.405342661={results.get('AR_ROSC_SLOPE')[2]}\
	&entry.2036291468={results.get('AR_ROSC_SLOPE')[3]}\
	&entry.1125126277={results.get('AR_ROSC_SLOPE')[4]}\
	&entry.509984940={results.get('AR_ROSC_SLOPE')[5]}\
	&entry.1518471801={results.get('AR_ROSC_SLOPE')[6]}\
	&entry.1010295649={results.get('AR_ROSC_SLOPE')[7]}\
	&entry.1658294866={results.get('AR_ROSC_SLOPE')[8]}\
	&entry.1700088219={results.get('AR_ROSC_SLOPE')[9]}\
	&entry.1990240042={results.get('AR_ROSC_SLOPE')[10]}\
	&entry.1994855141={results.get('AR_ROSC_SLOPE')[11]}\
	&entry.2004501020={results.get('AR_ROSC_SLOPE')[12]}\
	&entry.619680759={results.get('AR_ROSC_SLOPE')[13]}\
	&entry.1547920247={results.get('AR_ROSC_SLOPE')[14]}\
	&entry.112225409={results.get('AR_ROSC_SLOPE')[15]}\
	&entry.8615499={results.get('AR_ROSC_SLOPE')[16]}\
	&entry.447685801={results.get('AR_ROSC_SLOPE')[17]}\
	&entry.948996117={results.get('AR_ROSC_SLOPE')[18]}\
	&entry.549701779={results.get('AR_ROSC_SLOPE')[19]}\
	&entry.2034139644={results.get('AR_ROSC_SLOPE')[20]}\
	&entry.1738370945={results.get('AR_ROSC_SLOPE')[21]}\
	&entry.680984854={results.get('AR_ROSC_SLOPE')[22]}\
	&entry.380214201={results.get('AR_ROSC_SLOPE')[23]}\
	&entry.1949714184={results.get('AR_ROSC_SLOPE')[24]}\
	&entry.2080061991={results.get('AR_ROSC_SLOPE')[25]}\
	&entry.1355093371={results.get('AR_ROSC_SLOPE')[26]}\
	&entry.983676271={results.get('AR_ROSC_SLOPE')[27]}\
	&entry.1022530148={results.get('AR_ROSC_SLOPE')[28]}\
	&entry.2066074162={results.get('AR_ROSC_SLOPE')[29]}\
	&entry.1683950787={results.get('AR_ROSC_SLOPE')[30]}\
	&entry.1799042116={results.get('AR_ROSC_SLOPE')[31]}\
	&entry.352512380={results.get('AR_ROSC_SLOPE')[32]}\
	&entry.953608394={results.get('AR_ROSC_SLOPE')[33]}\
	&entry.1335702676={results.get('AR_ROSC_SLOPE')[34]}\
	&entry.1182244852={results.get('AR_ROSC_SLOPE')[35]}\
	&entry.869372092={results.get('AR_ROSC_SLOPE')[36]}\
	&entry.1109476155={results.get('AR_ROSC_SLOPE')[37]}\
	&entry.696844799={results.get('AR_ROSC_SLOPE')[38]}\
	&entry.881044474={results.get('AR_ROSC_SLOPE')[39]}\
	&entry.210472674={results.get('AR_ROSC_SLOPE')[40]}\
	&entry.1561547505={results.get('AR_ROSC_SLOPE')[41]}\
	&entry.294359514={results.get('AR_ROSC_OFFSET')[0]}\
	&entry.218278347={results.get('AR_ROSC_OFFSET')[1]}\
	&entry.1296340612={results.get('AR_ROSC_OFFSET')[2]}\
	&entry.325246147={results.get('AR_ROSC_OFFSET')[3]}\
	&entry.1461792727={results.get('AR_ROSC_OFFSET')[4]}\
	&entry.147717067={results.get('AR_ROSC_OFFSET')[5]}\
	&entry.308162325={results.get('AR_ROSC_OFFSET')[6]}\
	&entry.340294729={results.get('AR_ROSC_OFFSET')[7]}\
	&entry.1216091165={results.get('AR_ROSC_OFFSET')[8]}\
	&entry.1537892680={results.get('AR_ROSC_OFFSET')[9]}\
	&entry.651177331={results.get('AR_ROSC_OFFSET')[10]}\
	&entry.346475768={results.get('AR_ROSC_OFFSET')[11]}\
	&entry.1035896081={results.get('AR_ROSC_OFFSET')[12]}\
	&entry.2143379250={results.get('AR_ROSC_OFFSET')[13]}\
	&entry.923945135={results.get('AR_ROSC_OFFSET')[14]}\
	&entry.989723257={results.get('AR_ROSC_OFFSET')[15]}\
	&entry.971816065={results.get('AR_ROSC_OFFSET')[16]}\
	&entry.552958174={results.get('AR_ROSC_OFFSET')[17]}\
	&entry.739541542={results.get('AR_ROSC_OFFSET')[18]}\
	&entry.186269499={results.get('AR_ROSC_OFFSET')[19]}\
	&entry.502633129={results.get('AR_ROSC_OFFSET')[20]}\
	&entry.1532319666={results.get('AR_ROSC_OFFSET')[21]}\
	&entry.1786481368={results.get('AR_ROSC_OFFSET')[22]}\
	&entry.921537910={results.get('AR_ROSC_OFFSET')[23]}\
	&entry.91112264={results.get('AR_ROSC_OFFSET')[24]}\
	&entry.1403783859={results.get('AR_ROSC_OFFSET')[25]}\
	&entry.880466574={results.get('AR_ROSC_OFFSET')[26]}\
	&entry.255500529={results.get('AR_ROSC_OFFSET')[27]}\
	&entry.406968658={results.get('AR_ROSC_OFFSET')[28]}\
	&entry.252699286={results.get('AR_ROSC_OFFSET')[29]}\
	&entry.73007307={results.get('AR_ROSC_OFFSET')[30]}\
	&entry.22088182={results.get('AR_ROSC_OFFSET')[31]}\
	&entry.460622752={results.get('AR_ROSC_OFFSET')[32]}\
	&entry.987149730={results.get('AR_ROSC_OFFSET')[33]}\
	&entry.1559814776={results.get('AR_ROSC_OFFSET')[34]}\
	&entry.1700713522={results.get('AR_ROSC_OFFSET')[35]}\
	&entry.417646576={results.get('AR_ROSC_OFFSET')[36]}\
	&entry.1968942403={results.get('AR_ROSC_OFFSET')[37]}\
	&entry.1596668024={results.get('AR_ROSC_OFFSET')[38]}\
	&entry.2058648829={results.get('AR_ROSC_OFFSET')[39]}\
	&entry.1785914={results.get('AR_ROSC_OFFSET')[40]}\
	&entry.1316032248={results.get('AR_ROSC_OFFSET')[41]}",
    }
    log.info(
        bcolors.WARNING
        + "Copy the following URL into a browser to submit these results: \n"
        + url.get(outputDF.get("testType")).replace("\t", "")
        + "\n"
        + "View submitted results at: https://docs.google.com/spreadsheets/d/1pw_07F94fg2GJQr8wlvhaRUV63uhsAuBt_S1FEFBzBU/view"
        + bcolors.ENDC
    )
    with Path(outputfile).open("a") as fpointer:
        fpointer.writelines(url.get(outputDF.get("testType")).replace("\t", "") + "\n")
