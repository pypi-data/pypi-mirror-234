# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import os
import functools
import logging
import dataclasses

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
import numpy as np
import h5py
import fabio
from fabio.utils.cli import ProgressBar
import sys
from glob import glob
import argparse
from datetime import datetime
from xml.dom import minidom
import xml.etree.cElementTree as ET

from .yaml import make_yaml
from .edf_file_series import EdfFileSeries

APP_NAME = "h5-to-edf"

LRU_CACHE_SIZE = 64


logging.basicConfig()
_logger = logging.getLogger(APP_NAME)


@dataclasses.dataclass
class Config:
    """Contains the global configuration of the application"""

    edf_directory: str
    """Root directory where to store output data"""

    report: bool
    """If true, a report is displayed but the data is not processed"""

    process_dark: bool
    """If true, darks are processed"""

    process_flat: bool
    """If true, darks are processed"""

    generate_yml: bool
    """If true, a yaml file is generated from the scan metadata"""

    generate_xml: bool
    """If true, a xmlfile is generated from the scan metadata"""

    dry_run: bool
    """If true, the processing is done without writing anything"""

    args: object
    """Raw parsed arguments from the command line"""


class H5Handler:
    def __init__(self, h5filename: str, config: Config):
        self.h5_name = os.path.abspath(h5filename)
        self._config = config
        self.directory = os.path.dirname(self.h5_name)
        self.dataset = self.directory.split("/")[-1]
        self.flat = []
        self.dark = []
        self.static = []
        tmp = []
        with h5py.File(self.h5_name, "r") as f:
            for i in f:
                tmp.append(str(i))
                tmp = sorted(tmp, key=lambda x: int(x.split("_")[-1].split(".")[0]))
            for i in tmp:
                title = str(f[i]["title"][()])
                if "tomo" in title:
                    self.desc = str(i).split("_")[-1]
                if "dark" in title:
                    self.dark.append(str(i).split("_")[-1])
                if "flat" in title:
                    self.flat.append(str(i).split("_")[-1])
                if "projections" in title:
                    self.fast_acq = str(i).split("_")[-1].split(".")[0] + ".1"
                    self.slow_acq = str(i).split("_")[-1].split(".")[0] + ".2"
                if "static images" in title:
                    self.static.append(str(i).split("_")[-1])

        self.dataset_output = os.path.join(config.edf_directory, self.dataset + "_")

        self.dic_h5: dict[str, str] = {}
        try:
            with h5py.File(self.h5_name, "r") as f:
                info = [i for i in f][0]
                end_time = info + "/end_time"
                if end_time not in f:
                    raise Exception("Scan not over")
                values = [i for i in f]
                for value in values:
                    if value.split("_")[-1] not in self.dic_h5:
                        self.dic_h5[value.split("_")[-1]] = value

                try:
                    self.end_time = f[self.dic_h5[self.desc] + "/end_time"]()
                except:
                    pass

                if self.slow_acq not in self.dic_h5:
                    raise ValueError("Missing slow chain")

                self.detector = list(f[self.dic_h5[self.desc] + "/technique/detector"])[
                    0
                ]
                print(self.dic_h5[self.desc])

                try:
                    self.cameratype = f[
                        self.dic_h5[self.desc]
                        + f"/technique/detector/{self.detector}/name"
                    ][()]
                    self.cameratype = self.cameratype.decode()
                except AttributeError:
                    self.cameratype = self.cameratype

                except Exception:
                    try:
                        self.cameratype = f[
                            self.dic_h5[self.desc]
                            + f"/technique/detector/{self.detector}/type"
                        ][()]
                        self.cameratype = self.cameratype.decode()

                    except:
                        pass
                finally:
                    if "IRIS" in self.cameratype:
                        for i in f[self.dic_h5[self.desc] + "/technique/detector"]:
                            self.cameratype = i
                        # for i in f[self.dic_h5[self.fast_acq] + "/measurement/"]:
                        #    if i[:-1] == "iris" and int(i[-1]) in [1, 2, 3]:
                        #        print(i)
                        #        self.cameratype = i

                self.scantime = f[
                    self.dic_h5[self.fast_acq] + "/measurement/timer_trig"
                ][()]
                self.scancurrent = f[
                    self.dic_h5[self.slow_acq] + "/measurement/current"
                ][()]
                self.timecurrent = f[
                    self.dic_h5[self.slow_acq] + "/measurement/elapsed_time"
                ][()]

                sx = self.dic_h5[self.fast_acq] + "/instrument/positioners/sx"
                sy = self.dic_h5[self.fast_acq] + "/instrument/positioners/sy"
                yrot = self.dic_h5[self.fast_acq] + "/instrument/positioners/yrot"
                sz0 = self.dic_h5[self.fast_acq] + "/measurement/sz"
                sz1 = self.dic_h5[self.fast_acq] + "/instrument/positioners/sz"
                self.tomo_n = f[self.dic_h5[self.desc] + "/technique/scan/tomo_n"][()]
                self.digits = len(str(self.tomo_n))
                if self.digits < 4:
                    self.digits = 4

                self.positionners: dict[str, str | None] = {
                    "sx": None,
                    "sy": None,
                    "sz": None,
                    "yrot": None,
                }
                if sx in f:
                    self.positionners["sx"] = sx
                if sy in f:
                    self.positionners["sy"] = sy
                if yrot in f:
                    self.positionners["yrot"] = yrot
                if sz0 in f:
                    self.positionners["sz"] = sz0
                elif sz1 in f:
                    self.positionners["sz"] = sz1
                try:
                    self.ref_on = f[self.dic_h5[self.desc] + "/technique/scan/tomo_n"][
                        ()
                    ]
                except:
                    pass

                try:
                    self.acq_mode = f[
                        self.dic_h5[self.fast_acq]
                        + f"/instrument/{self.detector}/acq_parameters/acq_mode"
                    ][()]
                    self.max_expo = f[
                        self.dic_h5[self.fast_acq]
                        + f"/instrument/{self.detector}/ctrl_parameters/acc_max_expo_time"
                    ][()]
                    self.count_time = f[
                        self.dic_h5[self.fast_acq]
                        + f"/instrument/{self.detector}/acq_parameters/acq_expo_time"
                    ][()]
                    self.acq_frame = max(self.count_time / self.max_expo, 1)
                except:
                    _logger.debug("Error while reading acquisition info", exc_info=True)
                    _logger.error("Fall back with no acq_mode/acq_frame/max_expo")
                    self.acq_mode = ""
                    self.acq_frame = ""
                    self.max_expo = ""

                print("Accu= ", self.acq_frame)
        except AttributeError:
            pass

    def srot_position(self):
        with h5py.File(self.h5_name, "r") as f:
            if "mrsrot" in f[self.dic_h5[self.fast_acq] + "/measurement/"]:
                srot = f[self.dic_h5[self.fast_acq] + "/measurement/mrsrot"][()]
            elif "srot_eh2" in f[self.dic_h5[self.fast_acq] + "/measurement/"]:
                srot = f[self.dic_h5[self.fast_acq] + "/measurement/srot_eh2"][()]
        outname = os.path.join(self.dataset_output, "angle_proj.dat")
        if not self._config.dry_run:
            with open(outname, "w") as o:
                for value in srot:
                    o.write(f"{value:.8}\n")

    def create_info(self):
        with h5py.File(self.h5_name, "r") as f:
            ref_on = self.tomo_n
            n_flat = f[self.dic_h5[self.desc] + "/technique/scan/flat_n"][()]
            energy = f[self.dic_h5[self.desc] + "/technique/scan/energy"][()]
            distance = f[
                self.dic_h5[self.desc] + "/technique/scan/sample_detector_distance"
            ][()]
            scan_range = f[self.dic_h5[self.desc] + "/technique/scan/scan_range"][()]
            dark_n = f[self.dic_h5[self.desc] + "/technique/scan/dark_n"][()]
            if len(self.flat) > 0:
                y_step = f[self.dic_h5[self.flat[0]] + "/technique/flat/displacement"][
                    ()
                ]
            else:
                y_step = 0
            dim = f[
                self.dic_h5[self.desc] + f"/technique/detector/{self.detector}/size"
            ][()]
            tomo_exptime = f[self.dic_h5[self.desc] + "/technique/scan/exposure_time"][
                ()
            ]
            latency_time = f[self.dic_h5[self.desc] + "/technique/scan/latency_time"][
                ()
            ]
            roi = f[
                self.dic_h5[self.desc] + f"/technique/detector/{self.detector}/roi"
            ][()]
            try:
                acq_mode = f[
                    self.dic_h5[self.fast_acq]
                    + f"/instrument/{self.detector}/acq_parameters/acq_mode"
                ][()]
                max_expo = f[
                    self.dic_h5[self.fast_acq]
                    + f"/instrument/{self.detector}/ctrl_parameters/acc_max_expo_time"
                ][()]
                count_time = f[
                    self.dic_h5[self.fast_acq]
                    + f"/instrument/{self.detector}/acq_parameters/acq_expo_time"
                ][()]
                acq_frame = max(count_time / max_expo, 1)
            except:
                acq_mode = ""
                acq_frame = ""
                max_expo = ""
            col_end = roi[0]
            col_beg = roi[1]
            row_end = roi[2]
            row_beg = roi[3]
            pixelsize = f[
                self.dic_h5[self.desc] + "/technique/optic/sample_pixel_size"
            ][()]
            date = str(f[self.dic_h5[self.desc] + "/start_time"][()])
            srcurrent = f[self.dic_h5[self.desc] + "/instrument/machine/current"][()]
            try:
                comment = str(f[self.dic_h5[self.desc] + "/technique/scan/comment"][()])
            except:
                comment = ""

            print("Creation of the .info file")
            infofile = self.dataset_output + "/" + self.dataset + "_.info"
            if os.path.isfile(infofile):
                f = open(infofile, "r")
                lines = [line.strip("\n") for line in f.readlines()]
            else:
                lines = [""] * 40

            lines[1] = "Energy= " + str(energy)
            lines[2] = "Distance= " + str(distance)
            lines[3] = "Prefix= " + self.dataset
            lines[4] = "Directory= " + self.dataset_output
            lines[5] = "ScanRange= " + str(scan_range)
            lines[6] = "TOMO_N= " + str(ref_on)
            lines[7] = "REF_ON= " + str(ref_on)
            lines[8] = "REF_N= " + str(n_flat)
            lines[9] = "DARK_N= " + str(dark_n)
            lines[10] = "Y_STEP= " + str(y_step)
            lines[11] = "Dim_1= " + str(dim[0])
            lines[12] = "Dim_2= " + str(dim[1])
            lines[13] = "Count_time= " + str(tomo_exptime / 1000)
            lines[14] = "Latency_time (s)= " + str(latency_time / 1000)
            lines[16] = "Col_end= " + str(col_end)
            lines[17] = "Col_beg= " + str(col_beg)
            lines[18] = "Row_end= " + str(row_end)
            lines[19] = "Row_beg= " + str(row_beg)
            lines[21] = "PixelSize= " + str(pixelsize)
            lines[22] = "Optic_used= " + str(pixelsize)
            lines[23] = "Date= " + str(date[2:-1])
            lines[26] = "SrCurrent= " + str(f"{srcurrent:.3f}")
            lines[29] = "Acq_mode= " + str(acq_mode)
            lines[30] = "Acq_nb_frame= " + str("1")
            lines[31] = "Acq_orig= " + str(acq_frame)
            lines[32] = "Max_expo_time= " + str(max_expo)
            lines[38] = "Comment= " + str(comment[2:-1])

            if not self._config.dry_run:
                with open(infofile, "w") as filout:
                    for line in lines:
                        filout.write(line + "\n")

    def create_report(self):
        report_list = []
        with h5py.File(self.h5_name, "r") as f:
            # name
            report_list.append(f[self.dic_h5[self.desc] + "/technique/scan/name"][()])
            # date
            report_list.append(f[self.dic_h5[self.desc] + "/end_time"][()])
            # pixel size
            report_list.append(
                f[self.dic_h5[self.desc] + "/technique/optic/sample_pixel_size"][()]
            )
            # energy
            report_list.append(f[self.dic_h5[self.desc] + "/technique/scan/energy"][()])
            # current
            report_list.append(
                f[self.dic_h5[self.desc] + "/instrument/machine/current"][()]
            )
            # proj number
            report_list.append(f[self.dic_h5[self.desc] + "/technique/scan/tomo_n"][()])
            # duration
            end = f[self.dic_h5[self.desc] + "/end_time"][()]
            start = f[self.dic_h5[self.desc] + "/start_time"][()]
            end = datetime.fromisoformat(end.decode())
            start = datetime.fromisoformat(start.decode())
            duration = end - start
            duration_sec = duration.seconds
            report_list.append(duration_sec)
            report_list.append(duration_sec / 60)
            # xc
            xc = self.dic_h5[self.desc] + "/instrument/positioners/xc"
            report_list.append(xc)
            # sx
            sx = self.dic_h5[self.desc] + "/instrument/positioners/sx"
            report_list.append(sx)
            # sy
            sy = self.dic_h5[self.desc] + "/instrument/positioners/sy"
            report_list.append(sy)
            # sz
            sz = self.dic_h5[self.desc] + "/instrument/positioners/sz"
            report_list.append(sz)
            # yrot
            yrot = self.dic_h5[self.desc] + "/instrument/positioners/yrot"
            report_list.append(yrot)
            # HA
            # ???yrot/pixel_size
            # ct
            report_list.append(
                f[self.dic_h5[self.desc] + "/technique/scan/exposure_time"][()]
            )
            # range
            report_list.append(
                f[self.dic_h5[self.desc] + "/technique/scan/scan_range"][()]
            )
            # size proj
            size = f[
                self.dic_h5[self.desc] + f"/technique/detector/{self.detector}/size"
            ][()]
            report_list.append(size[0])
            report_list.append(size[1])
            # camera name
            report_list.append(
                f[self.dic_h5[self.desc] + f"/technique/detector/{self.detector}/name"][
                    ()
                ]
            )
            # acq mode
            report_list.append(
                f[
                    self.dic_h5[self.fast_acq]
                    + f"/instrument/{self.detector}/acq_parameters/acq_mode"
                ][()]
            )
            # Accumulation
            # ??? exp_time/subframe
            # Scintillator
            report_list.append(
                f[self.dic_h5[self.desc] + "/technique/optic/scintillator"][()]
            )
            # comments
            report_list.append(
                f[self.dic_h5[self.desc] + "/technique/scan/comment"][()]
            )

        return report_list

    def make_xml(self):
        print("Creation of the .xml file")
        with h5py.File(self.h5_name, "r") as f:
            tomo = ET.Element("tomo")

            acquisition = ET.SubElement(tomo, "acquisition")

            # beamline = ET.SubElement(acquisition, "beamline")
            # beamline.text = "BM18"

            # nameExp = ET.SubElement(acquisition, "nameExp")
            # nameExp.text = "tomo"

            scanName = ET.SubElement(acquisition, "scanName")
            scanName.text = f[self.dic_h5[self.desc] + "/sample/name"].asstr()[()]

            # disk = ET.SubElement(acquisition, "disk")
            # disk.text = "some vlaue2"

            date = ET.SubElement(acquisition, "date")
            date.text = f[self.dic_h5[self.desc] + "/end_time"].asstr()[()]

            machineMode = ET.SubElement(acquisition, "machineMode")
            machineMode.text = f[
                self.dic_h5[self.desc] + "/instrument/machine/filling_mode"
            ].asstr()[()]

            machineCurrentStart = ET.SubElement(acquisition, "machineCurrentStart")
            machineCurrentStart.text = str(
                f[self.dic_h5[self.desc] + "/instrument/machine/current"][()]
            )

            machineCurrentStop = ET.SubElement(acquisition, "machineCurrentStop")
            machineCurrentStop.text = str(self.scancurrent[-1])

            # insertionDeviceName = ET.SubElement(acquisition, "insertionDeviceName")
            # insertionDeviceName.text = "some value1"

            # insertionDeviceGap = ET.SubElement(acquisition, "insertionDeviceGap")
            # insertionDeviceGap.text = "some vlaue2"

            # filter = ET.SubElement(acquisition, "filter")
            # filter.text = "some value1"

            # monochromatorName = ET.SubElement(acquisition, "monochromatorName")
            # monochromatorName.text = "some vlaue2"

            energy = ET.SubElement(acquisition, "energy")
            energy.text = str(f[self.dic_h5[self.desc] + "/technique/scan/energy"][()])

            tomo_N = ET.SubElement(acquisition, "tomo_N")
            tomo_N.text = str(f[self.dic_h5[self.desc] + "/technique/scan/tomo_n"][()])

            ref_On = ET.SubElement(acquisition, "ref_On")
            ref_On.text = str(f[self.dic_h5[self.desc] + "/technique/scan/flat_on"][()])

            ref_N = ET.SubElement(acquisition, "ref_N")
            ref_N.text = str(f[self.dic_h5[self.desc] + "/technique/scan/flat_n"][()])

            dark_N = ET.SubElement(acquisition, "dark_N")
            dark_N.text = str(f[self.dic_h5[self.desc] + "/technique/scan/dark_n"][()])

            if len(self.flat) > 0:
                y_Step = ET.SubElement(acquisition, "y_Step")
                y_Step.text = str(
                    f[self.dic_h5[self.flat[0]] + "/technique/flat/displacement"][()]
                )

            # ccdtime = ET.SubElement(acquisition, "ccdtime")
            # ccdtime.text = "some vlaue2"

            # scanDuration = ET.SubElement(acquisition, "scanDuration")
            # scanDuration.text = "some value1"

            distance = ET.SubElement(acquisition, "distance")
            distance.text = str(
                f[self.dic_h5[self.desc] + "/technique/scan/sample_detector_distance"][
                    ()
                ]
            )

            sourceSampleDistance = ET.SubElement(acquisition, "sourceSampleDistance")
            sourceSampleDistance.text = str(
                f[self.dic_h5[self.desc] + "/technique/scan/source_sample_distance"][()]
            )

            scanRange = ET.SubElement(acquisition, "scanRange")
            scanRange.text = str(
                f[self.dic_h5[self.desc] + "/technique/scan/scan_range"][()]
            )

            scanType = ET.SubElement(acquisition, "scanType")
            scanType.text = f[
                self.dic_h5[self.desc] + "/technique/scan/scan_type"
            ].asstr()[()]

            # realFinalAngles = ET.SubElement(acquisition, "realFinalAngles")
            # realFinalAngles.text = "some vlaue2"

            opticsName = ET.SubElement(acquisition, "opticsName")
            opticsName.text = f[
                self.dic_h5[self.desc] + "/technique/optic/name"
            ].asstr()[()]

            scintillator = ET.SubElement(acquisition, "scintillator")
            scintillator.text = f[
                self.dic_h5[self.desc] + "/technique/optic/scintillator"
            ].asstr()[()]

            cameraName = ET.SubElement(acquisition, "cameraName")
            cameraName.text = self.cameratype

            cameraBinning = ET.SubElement(acquisition, "cameraBinning")
            cameraBinning.text = str(
                f[
                    self.dic_h5[self.desc]
                    + f"/technique/detector/{self.detector}/binning"
                ][()]
            )

            # cameraFibers = ET.SubElement(acquisition, "cameraFibers")
            # cameraFibers.text = "some vlaue2"

            pixelSize = ET.SubElement(acquisition, "pixelSize")
            pixelSize.text = str(
                f[
                    self.dic_h5[self.desc]
                    + f"/technique/detector/{self.detector}/pixel_size"
                ][()]
            )

            # ccdMode = ET.SubElement(acquisition, "ccdMode")
            # ccdMode.text = "some vlaue2"

            # projectionSize = ET.SubElement(acquisition, "projectionSize")
            # projectionSize.text = "some value1"

            listMotors = ET.SubElement(acquisition, "listMotors")
            listMotors.text = "motors"

            # ccdstatus = ET.SubElement(acquisition, "ccdstatus")
            # ccdstatus.text = "some value1"

            dom = minidom.parseString(ET.tostring(tomo))
            xml_str = dom.toprettyxml(indent="\t")
            outname = os.path.join(self.dataset_output, f"{scanName.text}_.xml")
            if not self._config.dry_run:
                with open(outname, "w") as fout:
                    fout.write(xml_str)

    def create_directory(self):
        if not os.path.isdir(self._config.edf_directory):
            cmd = "mkdir " + self._config.edf_directory
            if not self._config.dry_run:
                os.system(cmd)

        if not os.path.isdir(self.dataset_output):
            cmd = "mkdir " + self.dataset_output
            if not self._config.dry_run:
                os.system(cmd)

    def dump_files(self, data):
        print("Dumping files into", self.dataset_output)
        for filename in data.filename_list:
            outname = os.path.join(self.dataset_output, filename)
            if not self._config.dry_run:
                with open(outname, "wb") as fout:
                    fout.write(data[filename])

    def run_projection(self):
        """Creation of projections"""
        dataset = self.dic_h5[self.fast_acq] + "/measurement/" + self.cameratype
        sx = self.positionners["sx"]
        sy = self.positionners["sy"]
        sz = self.positionners["sz"]
        yrot = self.positionners["yrot"]
        ram_dump = False
        data = EdfFrom3d(
            self.h5_name,
            dataset,
            kind="proj",
            scan_time=self.scantime,
            current=self.scancurrent,
            time=self.timecurrent,
            acq_frame=self.acq_frame,
            sx=sx,
            sy=sy,
            sz=sz,
            yrot=yrot,
            filename_pattern=f"{self.dataset}_{{index:0{self.digits}d}}.edf",
            dump=ram_dump,
        )
        if ram_dump:
            data.dump_data("proj")
            try:
                self.dump_files(data)
            finally:
                data.close()
        else:
            series = EdfFileSeries(
                output_directory=self.dataset_output,
                filename_pattern=f"{self.dataset}_{{index:0{self.digits}d}}.edf",
            )
            progress = ProgressBar("Convert projections", self.tomo_n, 40)
            try:
                with series:
                    for i, _f, frame in data.iter_frames("proj"):
                        header = data.header(i)
                        series.append(frame, header)
                        progress.update(i)
            finally:
                progress.clear()
                data.close()

        try:
            last_frame = os.path.join(self.dataset_output, data.name(self.tomo_n - 1))
            very_last_frame = os.path.join(self.dataset_output, data.name(self.tomo_n))
            cmd = f"cp {last_frame} {very_last_frame}"
            print(cmd)
            if not self._config.dry_run:
                os.system(cmd)
        except Exception as e:
            _logger.debug("Error while duplicating the last proj", exc_info=True)
            print(e)

        print("Conversion of projections done")

    def run_dark(self):
        if len(self.dark) == 0:
            _logger.debug("No dark found")
            return
        dark = self.dark[0]
        if len(self.dark) > 1:
            _logger.warning(
                "More than one dark found. Only the first one was processed"
            )
        dataset = self.dic_h5[dark] + "/measurement/" + self.cameratype
        print("Conversion of darks in progress...")
        data = EdfFrom3d(
            self.h5_name,
            dataset,
            kind="dark",
            acq_frame=self.acq_frame,
            filename_pattern=f"dark.edf",
        )
        try:
            self.dump_files(data)
        finally:
            data.close()

        print("Conversion of darks done")

    def run_static(self):
        if len(self.static) == 0:
            _logger.debug("No static found")
            return
        if len(self.static) > 1:
            _logger.warning(
                "More than one static found. Only the first one was processed"
            )
        dataset = self.dic_h5[self.static[0]] + "/measurement/" + self.cameratype
        print("Conversion of end images in progress...")

        data = EdfFrom3d(
            self.h5_name,
            dataset,
            kind="static",
            acq_frame=self.acq_frame,
            filename_pattern=f"{self.dataset}_{{index:0{self.digits}d}}.edf",
            first_index=self.ref_on + 1,
        )

        try:
            self.dump_files(data)
        finally:
            data.close()

        # cmd = "mv " + self.dataset_output + "/static" + "0" * self.digits + ".edf " + self.dataset_output + "/static.edf"
        if not self._config.dry_run:
            # os.system(cmd)
            pass
        print("Conversion of end images done")

    def run_flat(self):
        if len(self.flat) == 0:
            _logger.debug("No flat found")
            return
        dataset = self.dic_h5[self.flat[0]] + "/measurement/" + self.cameratype
        print("Conversion of flats in progress...")
        data = EdfFrom3d(
            self.h5_name,
            dataset,
            kind="flat",
            acq_frame=self.acq_frame,
            filename_pattern=f"refHST{0:0{self.digits}d}.edf",
        )
        try:
            self.dump_files(data)
        finally:
            data.close()

        if len(self.flat) > 1:
            dataset = self.dic_h5[self.flat[1]] + "/measurement/" + self.cameratype
            print("Conversion of flats in progress...")
            data = EdfFrom3d(
                self.h5_name,
                dataset,
                kind="flat",
                acq_frame=self.acq_frame,
                filename_pattern=f"refHST{self.ref_on:0{self.digits}d}.edf",
            )
            try:
                self.dump_files(data)
            finally:
                data.close()
        else:
            try:
                cmd = (
                    f"cp {self.dataset_output}/refHST"
                    + "0" * self.digits
                    + f".edf {self.dataset_output}/refHST{self.ref_on:0{self.digits}d}.edf"
                )
                print(cmd)
                if not self._config.dry_run:
                    os.system(cmd)
            except Exception as e:
                _logger.debug("Error while copying refHST data", exc_info=True)
                print(
                    f"You might need to create {self.dataset_output}/{self.dataset}_{self.ref_on}.edf and {self.dataset_output}/refHST{self.ref_on:0{self.digits}d}.edf"
                )
                print(e)
        print("Conversion of flats done")

    def finish(self):
        cmd = f"chmod -R 777 {self.dataset_output}"
        if not self._config.dry_run:
            os.system(cmd)

    def execute(self):
        self.create_directory()
        self.run_projection()
        self.srot_position()
        self.run_static()
        if self._config.process_dark:
            self.run_dark()
        else:
            _logger.debug("Dark was skipped by configuration")

        if self._config.process_flat:
            self.run_flat()
        else:
            _logger.debug("Flat was skipped by configuration")

        self.create_info()

        if self._config.generate_xml:
            try:
                self.make_xml()
            except:
                _logger.debug("Error while generating XML file", exc_info=True)
                print("xml creation failed")

        if self._config.generate_yml:
            try:
                make_yaml(
                    self.h5_name, self.dataset_output, dry_run=self._config.dry_run
                )
            except:
                _logger.debug("Error while generating YAML file", exc_info=True)
                print("yaml creation failed")
        self.finish()

        print("Conversion over")


class EdfFrom3d:
    """Maps a 3D array in a hdf5 file to stack of 2D image files"""

    def __init__(
        self,
        h5filename,
        dataset,
        /,
        kind,
        acq_frame,
        scan_time=None,
        current=None,
        time=None,
        first_index=0,
        filename_pattern="{index:04d}.edf",
        sx=None,
        sy=None,
        sz=None,
        yrot=None,
        dump=True,
    ):
        """
        Arguments:
            h5filename: h5file to get the data from
            dataset: 3d array to map
            stem: output name stem
        """
        # FIXME: This is not properly handled
        self.h5o = h5py.File(h5filename, "r")
        self.dataset = self.h5o[dataset]
        assert len(self.dataset.shape) == 3, "We need a 3D array please!"

        self.current = None
        self.scan_time = scan_time
        self.time = time
        self.filename_pattern = filename_pattern
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.yrot = yrot
        self.first_index = first_index
        self.acq_frame = acq_frame
        self._file_size = None

        if kind == "proj":
            self.current = {}
            j = 0
            for i in range(len(self.scan_time)):
                while self.scan_time[i] > self.time[j] and j < len(self.time) - 1:
                    j += 1
                self.current[i] = current[j]

        if dump:
            self.dump_data(kind)

    def dump_data(self, kind):
        self.filename_list = []
        self.filename_lut = {}
        self.data = []
        for i, f, d in self.iter_frames(kind):
            self.filename_list.append(f)
            self.filename_lut[f] = i
            self.data.append(d)

    def iter_frames(self, kind):
        if kind == "dark":
            filename_list = [self.name(0)]
            if self.acq_frame > 1 and self.dataset.dtype == np.int32:
                data = np.array(
                    [np.mean(self.dataset, axis=0)] / self.acq_frame, dtype="float32"
                )
            else:
                data = np.array([np.mean(self.dataset, axis=0)], dtype="float32")

        elif kind == "flat":
            filename_list = [self.name(0)]
            if self.acq_frame > 1 and self.dataset.dtype == np.int32:
                data = np.array(
                    [np.median(self.dataset, axis=0)] / self.acq_frame, dtype="float32"
                )
            else:
                data = np.array([np.median(self.dataset, axis=0)], dtype="float32")

        elif kind == "static":
            filename_list = [self.name(i) for i in range(len(self))]
            if self.acq_frame > 1 and self.dataset.dtype == np.int32:
                data = np.array(self.dataset / self.acq_frame, dtype=np.uint16)
            else:
                data = self.dataset

        elif kind == "proj":
            # Decide on which frame has which filename:
            filename_list = [self.name(i) for i in range(len(self))]
            data = self.dataset

        else:
            assert False

        _logger.debug("Iter %s nb %s", len(filename_list), kind)
        for i, filename in enumerate(filename_list):
            yield i, filename, data[i]

    def close(self):
        self.dataset = None
        self.h5o.close()

    def name(self, i):
        """Generate some filename pattern"""
        index = int(self.first_index) + i
        return self.filename_pattern.format(index=index)

    def num(self, name):
        """Get the frame index from the filenane"""
        return self.filename_lut[name]

    def header(self, index):
        sx = self.sx
        sy = self.sy
        sz = self.sz
        yrot = self.yrot
        current = self.current

        result = {}
        if current is not None:
            if index >= len(current):
                result["SRCUR"] = str(current[len(current) - 1])
            else:
                result["SRCUR"] = str(current[index])
        if sx is not None and sy is not None and sz is not None and yrot is not None:
            motor_mne = []
            motor_pos = []
            if sx in self.h5o:
                motor_mne.append("sx")
                motor_pos.append(str(self.h5o[sx][()]))
            if sy in self.h5o:
                motor_mne.append("sy")
                motor_pos.append(str(self.h5o[sy][()]))
            if sz in self.h5o:
                motor_mne.append("sz")
                if "positioners" in sz:
                    motor_pos.append(str(self.h5o[sz][()]))
                else:
                    motor_pos.append(str(self.h5o[sz][()][index]))
            if yrot in self.h5o:
                motor_mne.append("yrot")
                motor_pos.append(str(self.h5o[yrot][()]))
            result["motor_mne"] = " ".join(motor_mne)
            result["motor_pos"] = " ".join(motor_pos)
        return result

    def toBlob(self, i):
        """Convert the numpy array to a file"""
        if self.acq_frame > 1 and self.data[i].dtype == np.int32:
            out = np.array(self.data[i] / self.acq_frame, dtype=np.uint16)
        else:
            out = np.array(self.data[i], dtype=np.uint16)

        header = self.header(i)
        edf = fabio.edfimage.edfimage(out, header=header)
        try:
            # FIXME: strange that we need to do this?
            edf._frames[0]._index = 0
            blob = bytearray(edf._frames[0].get_edf_block())
        except Exception as e:
            _logger.debug("Error while creating EDF output", exc_info=True)
            print(e)
        finally:
            edf.close()
        return blob

    def filesize(self, arg=0):
        """Size of the files"""
        if self._file_size is None:
            blob = self[arg]
            self._file_size = len(blob)
        return self._file_size

    # The rest is hopefully common to most 3D data arrays
    #  ... changes if you piece together scans in a h5 etc
    def __len__(self):
        """Number of frames"""
        return self.dataset.shape[0]

    @functools.lru_cache(maxsize=LRU_CACHE_SIZE)
    def __getitem__(self, arg):
        """
        Given a filename : return a Blob
        """
        if isinstance(arg, int):
            i = arg
        else:
            i = self.num(arg)  # raises KeyError if missing
        if i < 0 or i >= len(self):
            raise KeyError("Not found %s" % (arg))
        return self.toBlob(i)


def create_argument_parser():
    from . import __version__ as version

    parser = argparse.ArgumentParser()
    parser.add_argument("h5_names")
    parser.add_argument(
        "-o",
        dest="edf_directory",
        default=None,
        help="Output directory for EDF files",
    )
    # parser.add_argument('--start_nb', dest="start_nb", default=1)
    parser.add_argument(
        "--report",
        help="Display report without data processing",
        dest="report",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="Display debug information",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        help="Process the data without writing it",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"{APP_NAME} {version}"
    )
    parser.add_argument(
        "--no-dark",
        dest="process_dark",
        default=True,
        help="If the h5 does not contains darks, will skip dark creation",
        action="store_false",
    )
    parser.add_argument(
        "--no-flat",
        dest="process_flat",
        default=True,
        help="If the h5 does not contains flats, will skip flat creation",
        action="store_false",
    )
    parser.add_argument(
        "--yml",
        dest="generate_yml",
        default=False,
        help="Create a .yml file containing all the metadata from the h5 file",
        action="store_true",
    )
    parser.add_argument(
        "--no-xml",
        dest="generate_xml",
        default=True,
        help="Do not generate a .xml file containing few metadata from the h5 file",
        action="store_false",
    )
    return parser


def convert_h5_file_to_edf(h5_filename: str, config: Config):
    """Convert a specific HDF5 file into a EDF file structure"""
    print(f"Process {h5_filename}")
    directory = os.path.dirname(h5_filename)
    dataset = directory.split("/")[-1]
    dataset_output = os.path.join(config.edf_directory, dataset + "_")

    if os.path.exists(dataset_output):
        # FIXME: Check if correct number of files
        # FIXME: Check if right size of files
        _logger.error("EDF directory '%s' already exists: File skipped", dataset_output)
        return

    try:
        h5 = H5Handler(h5_filename, config)
    except ValueError as e:
        _logger.debug("Error while creating H5Handler", exc_info=True)
        _logger.error("%s: File skipped", e.args[0])
        return

    if "fast_acq" not in dir(h5) and "end_time" not in dir(h5):
        _logger.error("No fast_acq and no end_time in the file: File skipped")
        return

    if config.report:
        print(h5.create_report())
        return

    h5.execute()


def convert_to_edf() -> int:
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.debug:
        _logger.setLevel(logging.DEBUG)

    try:
        import resource
    except ImportError:
        _logger.debug("No resource module available")
    else:
        if hasattr(resource, "RLIMIT_NOFILE"):
            try:
                hard_nofile = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
                resource.setrlimit(resource.RLIMIT_NOFILE, (hard_nofile, hard_nofile))
            except (ValueError, OSError):
                _logger.warning("Failed to retrieve and set the max opened files limit")
            else:
                _logger.debug("Set max opened files to %d", hard_nofile)

    if "*" not in args.h5_names:
        if args.h5_names.endswith(".h5"):
            h5_names = [args.h5_names]
        else:
            if args.h5_names[-1] == "/":
                args.h5_names = args.h5_names[:-1]
            args.h5_names += "*"
    else:
        h5_names = [args.h5_names]

    if "*" in args.h5_names:
        h5_names = []
        for i in glob(args.h5_names):
            for j in glob(i + "/*.h5"):
                if "tomwer" not in j and "nabu" not in j:
                    h5_names.append(j)
        h5_names.sort()

    if h5_names == []:
        _logger.error("No HDF5 file found")
        return -1

    edf_directory = args.edf_directory
    if edf_directory is None:
        edf_directory = os.path.join(h5_names[0].split("RAW_DATA")[0], "NOBACKUP")

    config = Config(
        edf_directory=edf_directory,
        process_dark=args.process_dark,
        process_flat=args.process_flat,
        generate_yml=args.generate_yml,
        generate_xml=args.generate_xml,
        report=args.report,
        dry_run=args.dry_run,
        args=args,
    )

    # start_nb = args.start_nb
    if not os.path.exists(edf_directory):
        if not config.report and not config.dry_run:
            os.makedirs(edf_directory, exist_ok=True)

    _logger.debug("Found %s", h5_names)

    if not args.report:
        if not os.access(edf_directory, os.W_OK):
            _logger.error(
                "EDF directory '%s' not writtable: Processing cancelled", edf_directory
            )
            return -1

    for h5_name in h5_names:
        convert_h5_file_to_edf(h5_name, config)

    return 0


if __name__ == "__main__":
    res = convert_to_edf()
    sys.exit(res)
