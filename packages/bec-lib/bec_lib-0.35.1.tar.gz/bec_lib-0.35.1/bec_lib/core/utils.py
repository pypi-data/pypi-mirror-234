from __future__ import annotations

import csv
import functools
from collections import defaultdict
from typing import TYPE_CHECKING, List, Union

from typeguard import typechecked

if TYPE_CHECKING:
    from bec_lib.scan_manager import ScanReport


def threadlocked(fcn):
    """Ensure that the thread acquires and releases the lock."""

    @functools.wraps(fcn)
    def wrapper(self, *args, **kwargs):
        # pylint: disable=protected-access
        with self._lock:
            return fcn(self, *args, **kwargs)

    return wrapper


@typechecked
def scan_to_csv(
    scan_report: Union[ScanReport, List[ScanReport]],
    output_name: str,
    delimiter: str = ",",
    dialect: str = None,
    header: list = None,
    write_metadata: bool = True,
) -> None:
    """Convert scan data to a csv file.

    Args:
        scan_report (ScanReport): Scan report object.
        filename (str): Name of the csv file.
        delimiter (str, optional): Delimiter for the csv file. Defaults to ",".
        dialect (str, optional): Argument for csv.Dialect. Defaults to None. E.g. 'excel', 'excel_tab' or 'unix_dialect', still takes argument from delimiter, choose delimier='' to omit
        header (list, optional): Create custom header for the csv file. If None, header is created automatically. Defaults to None.
        write_metadata (bool, optional): If True, the metadata of the scan will be written to the header of csv file. Defaults to True.

    Examples:
        >>> scan_to_csv(scan_report, "./scan.csv")
    """
    if isinstance(scan_report, ScanReport):
        scan_report = [scan_report]
    header_out = []
    body_out = []
    data_output = []

    for scan_rep in scan_report:
        header_tmp, body_tmp = _extract_scan_data(
            scan_report=scan_rep, header=header, write_metadata=write_metadata
        )
        header_out.extend(header_tmp[:-1])
        body_out.extend(body_tmp)
    header_out.append(header_tmp[-1])  # To only append the header keys once
    data_output.extend(header_out)
    data_output.extend(body_out)

    _write_csv(
        output_name=output_name,
        delimiter=delimiter,
        dialect=dialect,
        output=data_output,
    )


def _write_csv(
    output_name: str,
    delimiter: str,
    output: list,
    dialect: str = None,
) -> None:
    """Write csv file.

    Args:
        output_name (str): Name of the csv file.
        delimiter (str): Delimiter for the csv file.
        dialect (str): Argument for csv.Dialect. Defaults to None. If no None, delimiter input is ignored. Some input examples 'excel', 'excel_tab' or 'unix_dialect'
        data_dict (dict): Dictionary to be written to csv.

        Examples:
            >>> _write_csv("./scan.csv", ",", ["#samx", "bpm4i"], True, scan_dict)
    """

    with open(output_name, "w", encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter=delimiter, dialect=dialect)
        writer.writerows(output)


def _extract_scan_data(
    scan_report: ScanReport,
    header: list = None,
    write_metadata: bool = True,
) -> tuple:
    """Extract scan data from scan report.

    Args:
        scan_report (ScanReport): Scan report object.
        header (list, optional): Create custom header for the csv file. If None, header is created automatically. Defaults to None.
        write_metadata (bool, optional): If True, the metadata of the scan will be written to the header of csv file. Defaults to True.

    Returns:
        (tuple): Tuple of header and body of the csv file.
    """
    scan_dict = scan_to_dict(scan_report, flat=True)

    header_tmp = [["#" + entry.replace("\t", "")] for entry in str(scan_report).split("\n")]
    if write_metadata:
        header_tmp.append(["#ScanMetadata"])
        scan_metadata = scan_report.scan.data[list(scan_report.scan.data.keys())[-1]].metadata
        for key, value in scan_metadata.items():
            header_tmp.append(["".join(["#", key]), value])
    if header:
        header_keys = header
    else:
        header_keys = ["scan_number", "dataset_number"]
        [
            header_keys.extend([f"{value}_value", f"{time}_timestamp"])
            for value, time in zip(scan_dict["value"].keys(), scan_dict["timestamp"].keys())
        ]
    header_keys[0] = "".join(["#", header_keys[0]])
    header_tmp.append(header_keys)

    body_tmp = []
    num_entries = len(list(scan_dict["value"].values())[0])
    for ii in range(num_entries):
        sub_list = []
        sub_list.extend([scan_metadata["scan_number"], scan_metadata["dataset_number"]])
        for key in scan_dict["value"]:
            sub_list.extend([scan_dict["value"][key][ii], scan_dict["timestamp"][key][ii]])
        body_tmp.append(sub_list)

    return header_tmp, body_tmp


def scan_to_dict(scan_report: ScanReport, flat: bool = True) -> dict:
    """Convert scan data to a dictionary.

    Args:
        scan_report (ScanReport): Scan report object.
        flat (bool, optional): If True, the dictionary will be flat. Defaults to True.

    Returns:
        (dict): Dictionary of scan data.

    Examples:
        >>> scan_to_dict(scan_report) with scan_report = scans.line_scan(...)
    """
    if flat:
        scan_dict = {"timestamp": defaultdict(lambda: []), "value": defaultdict(lambda: [])}
    else:
        scan_dict = {
            "timestamp": defaultdict(lambda: defaultdict(lambda: [])),
            "value": defaultdict(lambda: defaultdict(lambda: [])),
        }

    for scan_msg in scan_report.scan.data.values():
        scan_msg_data = scan_msg.content["data"]
        for dev, dev_data in scan_msg_data.items():
            for signal, signal_data in dev_data.items():
                if flat:
                    scan_dict["timestamp"][signal].append(signal_data["timestamp"])
                    scan_dict["value"][signal].append(signal_data["value"])
                else:
                    scan_dict["timestamp"][dev][signal].append(signal_data["timestamp"])
                    scan_dict["value"][dev][signal].append(signal_data["value"])

    return scan_dict
