# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import os
import h5py
import numpy as np

try:
    import yaml
except ImportError:
    yaml = None


def make_yaml(h5_name: str, dataset_output: str, dry_run: bool = False) -> None:
    """
    Create a YAML file from an HDF5 file.

    Parameters:
    h5_name (str): The name of the HDF5 file.
    dataset_output (str): The directory where the YAML file will be saved.

    Returns:
    None
    """
    if yaml is None:
        raise RuntimeError("PyYAML is not installed")

    if not h5_name.endswith(".h5"):
        raise ValueError("The input file is not a .h5 file")

    print("Creation of the .yml file")

    dark = []
    flat = []
    static = []

    with h5py.File(h5_name, "r") as f:
        # Get a list of all the groups in the HDF5 file
        values = [i for i in f]
        # Create a dictionary that maps the last part of the group name to the full group name
        dic_h5 = {}
        for value in values:
            if value.split("_")[-1] not in dic_h5:
                dic_h5[value.split("_")[-1]] = value

        tmp = sorted(dic_h5.keys(), key=lambda x: int(x.split(".")[-1]))
        for i in tmp:
            title = str(f[dic_h5[i]]["title"][()])
            if "tomo" in title:
                desc = i
            if "dark" in title:
                dark.append(i)
            if "flat" in title:
                flat.append(i)
            if "projections" in title:
                fast_acq = i.split(".")[0] + ".1"
                slow_acq = i.split(".")[0] + ".2"
            if "static images" in title:
                static.append(i)

        # Get acquisition parameters
        detector = list(f[dic_h5[desc] + "/technique/detector"])[0]
        count_time = _safe_hdf5_read(
            f, dic_h5[fast_acq] + f"/instrument/{detector}/acq_parameters/acq_expo_time"
        )
        max_expo = _safe_hdf5_read(
            f,
            dic_h5[fast_acq]
            + f"/instrument/{detector}/ctrl_parameters/acc_max_expo_time",
        )

        # Create the YAML data structure
        data = {
            "tomo": {
                "acquisition": {
                    "scanName": _safe_hdf5_read(f, dic_h5[desc] + "/sample/name"),
                    "date": _safe_hdf5_read(f, dic_h5[desc] + "/end_time"),
                    "beamline": _safe_hdf5_read(
                        f, dic_h5[desc] + f"/technique/saving/beamline"
                    ),
                    "machineMode": _safe_hdf5_read(
                        f, dic_h5[desc] + "/instrument/machine/filling_mode"
                    ),
                    "machineCurrentStart": _safe_hdf5_read(
                        f, dic_h5[desc] + "/instrument/machine/current"
                    ),
                    "machineCurrentStop": float(
                        f[dic_h5[slow_acq] + "/measurement/current"][()][-1]
                    ),
                    "distance": str(
                        round(
                            float(
                                _safe_hdf5_read(
                                    f,
                                    dic_h5[desc]
                                    + "/technique/scan/sample_detector_distance",
                                )
                            ),
                            2,
                        )
                    ),
                    "sourceSampleDistance": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/source_sample_distance"
                    ),
                    "energy": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/energy"
                    ),
                    "tomo_N": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/tomo_n"
                    ),
                    "ref_On": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/flat_on"
                    ),
                    "ref_N": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/flat_n"
                    ),
                    "dark_N": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/dark_n"
                    ),
                    "scanRange": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/scan_range"
                    ),
                    "scanType": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/scan_type"
                    ),
                    "half_acquisition": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/half_acquisition"
                    ),
                    "comment": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/comment"
                    ),
                    "nb_scans": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/nb_scans"
                    ),
                    "delta_z": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/scan/delta_pos"
                    ),
                    "opticsName": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/optic/name"
                    ),
                    "scintillator": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/optic/scintillator"
                    ),
                    "magnification": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/optic/magnification"
                    ),
                    "cameraType": _safe_hdf5_read(
                        f, dic_h5[desc] + f"/technique/detector/{detector}/type"
                    ),
                    "cameraBinning": _safe_hdf5_read(
                        f, dic_h5[desc] + f"/technique/detector/{detector}/binning"
                    ),
                    "pixelSize": _safe_hdf5_read(
                        f, dic_h5[desc] + "/technique/optic/sample_pixel_size"
                    ),
                    "roi_size": _safe_hdf5_read(
                        f, dic_h5[desc] + f"/technique/detector/{detector}/size"
                    ),
                    "acq_mode": _safe_hdf5_read(
                        f,
                        dic_h5[fast_acq]
                        + f"/instrument/{detector}/acq_parameters/acq_mode",
                    ),
                    "expo_time": count_time,
                    "subframe": max_expo,
                    "latency_time": _safe_hdf5_read(
                        f, dic_h5[fast_acq] + f"/technique/proj/latency_time"
                    ),
                    "accumulation": float(max(count_time / max_expo, 1)),
                    "scan_time": float(
                        f[dic_h5[fast_acq] + f"/measurement/timer_trig"][()][-1]
                    ),
                }
            }
        }

        # Create a dictionary of motors
        motors = {}
        for name in f[dic_h5[desc] + "/instrument/positioners/"].keys():
            motors[name] = _safe_hdf5_read(
                f, dic_h5[desc] + f"/instrument/positioners/{name}"
            )
        data["tomo"]["acquisition"]["motors"] = motors

        # Save the YAML file
        scan_name = (f[dic_h5[desc] + "/sample/name"][()]).decode("utf-8")
        outname = os.path.join(dataset_output, f"{scan_name}_.yml")
        if not dry_run:
            with open(outname, "w") as yamlfile:
                yaml.safe_dump(
                    data, yamlfile, default_flow_style=False, sort_keys=False
                )


def _safe_hdf5_read(hdf_file, key, default=None):
    """
    Read a value from an HDF5 file and return a safe representation of the value.

    Parameters:
    hdf_file (h5py.File): The HDF5 file object.
    key (str): The key to read from the HDF5 file.
    default (any): The default value to return if the key is not found.

    Returns:
    The value associated with the key, or the default value if the key is not found.
    """
    try:
        value = hdf_file[key][()]
        if isinstance(value, bytes):
            return value.decode("utf-8")
        elif isinstance(value, (float, np.float64, np.float32, np.int64)):
            return float(value)
        else:
            return str(value)
    except KeyError:
        return default
