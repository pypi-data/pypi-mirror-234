from __future__ import annotations

import json
import logging
from glob import glob
from pathlib import Path

import typer
from module_qc_data_tools import (
    check_sn_format,
    convert_name_to_serial,
    get_layer_from_sn,
)

from module_qc_analysis_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_analysis_tools.utils.analysis import (
    get_n_chips,
)
from module_qc_analysis_tools.utils.classification import (
    required_tests,
)
from module_qc_analysis_tools.utils.misc import (
    bcolors,
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

results_from_scans = {
    "std_digitalscan": ["OccupancyMap"],
    "std_analogscan": ["OccupancyMap", "MeanTotMap"],
    "std_thresholdscan_hr": ["Chi2Map", "ThresholdMap", "NoiseMap", "Config"],
    "std_thresholdscan_hd": ["Chi2Map", "ThresholdMap", "NoiseMap", "Config"],
    "std_noisescan": ["NoiseOccupancy", "Config"],
    "std_totscan": ["MeanTotMap"],
    "std_discbumpscan": ["OccupancyMap", "Config"],
    "std_mergedbumpscan": ["OccupancyMap", "Config"],
    "std_thresholdscan_zerobias": ["Chi2Map", "ThresholdMap", "NoiseMap", "Config"],
    "selftrigger_source": ["Occupancy", "Config"],
}


def findLatestResults(path, tests):
    path = str(path.resolve())

    log.debug(f"Searching for latest YARR scan results in {path} for {tests}")
    alldirs = glob(path + "/*")
    alldirs.sort()

    # Make structure to hold location of results
    latest_results = {}
    for t in tests:
        if t not in results_from_scans.keys():
            continue  # Only save scans that we will use for analysis
        latest_results.update({t: "null"})

    # Find latest YARR scans, assumes directories named with run numbers
    for d in alldirs:
        if "last_scan" in d:
            alldirs.remove(d)
        for s in latest_results:
            if s in d:
                latest_results.update({s: d})
                break
    return latest_results


def getDataFile(mname, latest_results, test_name, n_chips):
    log.debug(f"Setting module SN to {mname}")
    # Setup structure of output
    config_file = {
        "datadir": "",  # Full paths are stored for each file now
        "module": {"serialNumber": mname, "chipType": "RD53B"},
        "chip": [],
    }

    # Collect necessary data from each scan
    chip_data = {}
    for scan in latest_results:
        if latest_results.get(scan) == "null":
            if "discbump" in scan:
                log.warning(
                    bcolors.WARNING + f"No results for {scan} found." + bcolors.ENDC
                )
                continue
            log.error(
                bcolors.BADRED
                + f"No results for {scan} found! This is required for {test_name}. Please fix."
                + bcolors.ENDC
            )
            raise RuntimeError()
        log.debug(f"Searching for {scan} scans")
        for v in results_from_scans.get(scan):
            if v == "Config":
                data = glob(latest_results.get(scan) + "/0x*.json.before")
            else:
                data = glob(latest_results.get(scan) + "/*_" + v + "*.json")

            # Check data that was found
            if len(data) == 0:
                log.error(
                    bcolors.BADRED
                    + f"No results found for {v} in {latest_results.get(scan)} - please fix!"
                    + bcolors.ENDC
                )
                raise RuntimeError()
            if len(data) != n_chips:
                log.error(
                    bcolors.WARNING
                    + f"Found {len(data)} results for {v} in {latest_results.get(scan)}, but results from {n_chips} chips expected! Please be aware that you are missing data from at least one chip:."
                    + bcolors.ENDC
                )
                log.error(bcolors.WARNING + f"{data}" + bcolors.ENDC)

            for d in data:
                log.debug(f"Found {d}")
                chipname = d.split("/")[-1].split("_")[0]
                if chip_data.get(chipname):
                    chip_data[chipname]["filepaths"].update(
                        {scan.replace("std_", "") + "_" + v: d}
                    )
                else:
                    chip_data[chipname] = {
                        "serialNumber": convert_name_to_serial(chipname),
                        "filepaths": {scan.replace("std_", "") + "_" + v: d},
                    }
    for r in chip_data:
        config_file["chip"].append(chip_data[r])
        log.info(
            f"Found {len(chip_data[r]['filepaths'])} YARR scans for chip {chip_data[r].get('serialNumber')}"
        )

    return config_file


app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    output_yarr: Path = OPTIONS["output_yarr"],
    module_sn: str = OPTIONS["moduleSN"],
    verbosity: LogLevel = OPTIONS["verbosity"],
    test_name: str = OPTIONS["test_name"],
    digitalscan: Path = OPTIONS["digitalscan"],
    analogscan: Path = OPTIONS["analogscan"],
    thresholdscan_hr: Path = OPTIONS["thresholdscan_hr"],
    thresholdscan_hd: Path = OPTIONS["thresholdscan_hd"],
    noisescan: Path = OPTIONS["noisescan"],
    totscan: Path = OPTIONS["totscan"],
    thresholdscan_zerobias: Path = OPTIONS["thresholdscan_zerobias"],
    discbumpscan: Path = OPTIONS["discbumpscan"],
    mergedbumpscan: Path = OPTIONS["mergedbumpscan"],
    sourcescan: Path = OPTIONS["sourcescan"],
):
    log.setLevel(verbosity.value)

    log.info("")
    log.info(" ==============================================================")
    log.info(f" \tCollecting YARR scan output for module {module_sn}")
    log.info(" ==============================================================")
    log.info("")

    check_sn_format(module_sn)
    nChips = get_n_chips(get_layer_from_sn(module_sn))
    collect_tests = required_tests.get(test_name)
    if not collect_tests:
        log.error(
            bcolors.BADRED
            + f"{test_name} not recognized! Must be one of: {required_tests.keys()}"
            + bcolors.ENDC
        )
        raise RuntimeError()

    # Find latest results if path to all YARR output is supplied
    latest_results = {}

    # Fill in user-supplied YARR output directories
    if digitalscan is not None:
        latest_results.update({"std_digitalscan": str(digitalscan.resolve())})
    if analogscan is not None:
        latest_results.update({"std_analogscan": str(analogscan.resolve())})
    if thresholdscan_hr is not None:
        latest_results.update({"std_thresholdscan_hr": str(thresholdscan_hr.resolve())})
    if thresholdscan_hd is not None:
        latest_results.update({"std_thresholdscan_hd": str(thresholdscan_hd.resolve())})
    if noisescan is not None:
        latest_results.update({"std_noisescan": str(noisescan.resolve())})
    if thresholdscan_zerobias is not None:
        latest_results.update(
            {"std_thresholdscan_zerobias": str(thresholdscan_zerobias.resolve())}
        )
    if totscan is not None:
        latest_results.update({"std_totscan": str(totscan.resolve())})
    if discbumpscan is not None:
        latest_results.update({"std_discbumpscan": str(discbumpscan.resolve())})
    if mergedbumpscan is not None:
        latest_results.update({"std_mergedbumpscan": str(mergedbumpscan.resolve())})
    if sourcescan is not None:
        latest_results.update({"selftrigger_source": str(sourcescan.resolve())})

    if len(latest_results.keys()) == 0:
        log.error(
            "No YARR results found. Please specify directory to latest YARR scan results, or supply each YARR scan output with appropriate flags. Type `analysis-load-yarr-scans -h` for help"
        )
        raise RuntimeError()

    output_json = getDataFile(module_sn, latest_results, test_name, nChips)

    # Write to output
    with Path(str(output_yarr) + f"/info_{test_name}.json").open("w") as f:
        log.info("Writing " + str(output_yarr) + f"/info_{test_name}.json")
        json.dump(
            output_json,
            f,
            ensure_ascii=False,
            indent=4,
            sort_keys=False,
            separators=(",", ": "),
        )


if __name__ == "__main__":
    main()
