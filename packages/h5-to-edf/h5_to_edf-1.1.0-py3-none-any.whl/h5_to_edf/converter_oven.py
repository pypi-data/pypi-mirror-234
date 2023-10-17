# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import os
import functools

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
import numpy as np
import h5py
import fabio
import sys
from glob import glob
import argparse
from datetime import datetime
from xml.dom import minidom
import xml.etree.cElementTree as ET
import re

LRU_CACHE_SIZE = 64


class H5Handler(object):
    def __init__(self, h5filename, edf_directory):
        self.h5_name = os.path.abspath(h5filename)
        self.directory = os.path.dirname(self.h5_name)
        self.edf_directory = edf_directory
        self.dataset = self.directory.split("/")[-1]
        self.flat = []
        self.dark = []
        self.static = []
        tmp = []
        self.find_flat()
        self.find_dark()
        with h5py.File(self.h5_name, "r") as f:
            for i in f:
                tmp.append(str(i))
                tmp = sorted(tmp, key=lambda x: int(x.split("_")[-1].split(".")[0]))
            for i in tmp:
                title = str(f[i]["title"][()])
                if "tomo" in title:
                    self.desc = str(i).split("_")[-1]
                if "projections" in title:
                    self.fast_acq = str(i).split("_")[-1].split(".")[0] + ".1"
                    self.slow_acq = str(i).split("_")[-1].split(".")[0] + ".2"
                if "static images" in title:
                    self.static.append(str(i).split("_")[-1])
        self.dataset_output = os.path.join(edf_directory, self.dataset + "_")

        try:
            with h5py.File(self.h5_name, "r") as f:
                info = [i for i in f][0]
                end_time = info + "/end_time"
                if end_time not in f:
                    f.close()
                    raise Exception("Scan not over")
                values = [i for i in f]
                self.dic_h5 = {}
                for value in values:
                    self.dic_h5[value.split("_")[-1]] = value

                try:
                    self.end_time = f[self.dic_h5[self.desc] + "/end_time"]()
                except:
                    pass

                if self.slow_acq not in self.dic_h5:
                    delattr(self, "fast_acq")
                    print("Missing slow chain")
                    return
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
                        if "IRIS" in self.cameratype:
                            self.cameratype = "iris1"

                    except:
                        pass

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
                sz0 = self.dic_h5[self.fast_acq] + "/measurement/sz"
                sz1 = self.dic_h5[self.fast_acq] + "/instrument/positioners/sz"
                self.tomo_n = f[self.dic_h5[self.desc] + "/technique/scan/tomo_n"][()]
                self.digits = len(str(self.tomo_n))
                if self.digits < 4:
                    self.digits = 4

                self.positionners = {"sx": None, "sy": None, "sz": None}
                if sx in f:
                    self.positionners["sx"] = sx
                if sy in f:
                    self.positionners["sy"] = sy
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
                    print("Error !!!!!!!!")
                    self.acq_mode = ""
                    self.acq_frame = ""
                    self.max_expo = ""

                print("Accu= ", self.acq_frame)
        except AttributeError:
            pass

    def find_flat(self):
        path, name = os.path.split(os.path.split(self.h5_name)[0])
        regex = re.compile("[0-9]+?.*?um")
        um = regex.findall(name)[0]
        if name[-1] == "w" or name[-1].isnumeric():
            cont = glob(os.path.join(path, f"*{um}*flat*"))
        else:
            cont = glob(os.path.join(path, f"*{um}*flat*{name[-1]}"))
        regex = re.compile("[0-9]+C")
        temp = int(regex.findall(name)[0][:-1])
        diff = 9999
        for i in cont:
            val = int(regex.findall(i)[0][:-1])
            if abs(val - temp) < diff:
                diff = abs(val - temp)
                res = i
        h5 = glob(res + "/*.h5")
        self.flat_name = h5[0]
        self.flat = ["1.1"]
        # raise Exception

    def find_dark(self):
        path, name = os.path.split(os.path.split(self.h5_name)[0])
        regex = re.compile("[0-9]*?.[0-9]*?um")
        um = regex.findall(name)[0]
        cont = glob(os.path.join(path, f"*{um}*dark"))[0]
        h5 = glob(os.path.join(cont, "*.h5"))
        self.dark_name = h5[0]
        self.dark = ["1.1"]

    def srot_position(self):
        with h5py.File(self.h5_name, "r") as f:
            if "mrsrot" in f[self.dic_h5[self.fast_acq] + "/measurement/"]:
                srot = f[self.dic_h5[self.fast_acq] + "/measurement/mrsrot"][()]
            elif "srot_eh2" in f[self.dic_h5[self.fast_acq] + "/measurement/"]:
                srot = f[self.dic_h5[self.fast_acq] + "/measurement/srot_eh2"][()]
        outname = os.path.join(self.dataset_output, "angle_proj.dat")
        with open(outname, "w") as o:
            for value in srot:
                o.write(f"{value:.8}\n")

    def create_info(self):
        with h5py.File(self.flat_name, "r") as f:
            if len(self.flat) > 0:
                y_step = f["1.1/technique/flat/displacement"][()]
                if not isinstance(y_step, str):
                    y_step = y_step[0]
            else:
                y_step = ""

        with h5py.File(self.h5_name, "r") as f:
            ref_on = self.tomo_n
            n_flat = f[self.dic_h5[self.desc] + "/technique/scan/flat_n"][()]
            energy = f[self.dic_h5[self.desc] + "/technique/scan/energy"][()]
            distance = f[
                self.dic_h5[self.desc] + "/technique/scan/sample_detector_distance"
            ][()]
            scan_range = f[self.dic_h5[self.desc] + "/technique/scan/scan_range"][()]
            dark_n = f[self.dic_h5[self.desc] + "/technique/scan/dark_n"][()]

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
            scantype = str(
                f[self.dic_h5[self.desc] + "/technique/scan/field_of_view"][()]
            )
            yrot = f[self.dic_h5[self.desc] + "/instrument/positioners/yrot"][()]
            # Creation of scan.info

            print("Creation of the .info file")
            infofile = self.dataset_output + "/" + self.dataset + "_.info"
            if os.path.isfile(infofile):
                f = open(infofile, "r")
                lines = [
                    line.strip("\n") for line in f.readlines()
                ]  # on retire les \n en fin de ligne avec strip('\n')
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

            if os.path.isfile(infofile):
                f.close()

                # infofile='EDF/'+dataset+'/'+dataset+'good.info'
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
            scanName.text = f[self.dic_h5[self.desc] + "/sample/name"][()].decode()

            # disk = ET.SubElement(acquisition, "disk")
            # disk.text = "some vlaue2"

            date = ET.SubElement(acquisition, "date")
            date.text = f[self.dic_h5[self.desc] + "/end_time"][()].decode()

            machineMode = ET.SubElement(acquisition, "machineMode")
            machineMode.text = f[
                self.dic_h5[self.desc] + "/instrument/machine/filling_mode"
            ][()].decode()

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

            # if len(self.flat) > 0:
            # y_Step = ET.SubElement(acquisition, "y_Step")
            # y_Step.text = str(f[self.dic_h5[self.flat[
            # 0]] + "/technique/flat/displacement"][()])

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
            scanType.text = f[self.dic_h5[self.desc] + "/technique/scan/scan_type"][
                ()
            ].decode()

            # realFinalAngles = ET.SubElement(acquisition, "realFinalAngles")
            # realFinalAngles.text = "some vlaue2"

            opticsName = ET.SubElement(acquisition, "opticsName")
            opticsName.text = f[self.dic_h5[self.desc] + "/technique/optic/name"][
                ()
            ].decode()

            scintillator = ET.SubElement(acquisition, "scintillator")
            scintillator.text = f[
                self.dic_h5[self.desc] + "/technique/optic/scintillator"
            ][()].decode()

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
            outname = os.path.join(self.dataset_output, f"{scanName.text}.xml")
            with open(outname, "w") as fout:
                fout.write(xml_str)

    def create_directory(self):
        if not os.path.isdir(self.edf_directory):
            cmd = "mkdir " + self.edf_directory
            os.system(cmd)

        if not os.path.isdir(self.dataset_output):
            cmd = "mkdir " + self.dataset_output
            os.system(cmd)

    def dump_files(self, data):
        print("Dumping files into", self.dataset_output)
        # tmp_c = 0
        for filename in data.filename_list:
            outname = os.path.join(self.dataset_output, filename)
            with open(outname, "wb") as fout:
                fout.write(data[filename])

    def run_projection(self):
        # Creation of projections
        # edf_converter(self.dataset_output, self.h5_name, self.dataset, self.scantime, self.scancurrent, self.timecurrent, self.positionners)
        dataset = self.dic_h5[self.fast_acq] + "/measurement/" + self.cameratype
        sx = self.positionners["sx"]
        sy = self.positionners["sy"]
        sz = self.positionners["sz"]
        data = EdfFrom3d(
            self.h5_name,
            dataset,
            self.scantime,
            self.scancurrent,
            self.timecurrent,
            acq_frame=self.acq_frame,
            sx=sx,
            sy=sy,
            sz=sz,
            stem=self.dataset,
            digits=self.digits,
        )
        self.dump_files(data)
        try:
            last_proj = self.ref_on - 1
            cmd = f"cp {self.dataset_output}/{self.dataset}_{last_proj:0{self.digits}d}.edf {self.dataset_output}/{self.dataset}_{self.ref_on:0{self.digits}d}.edf"
            os.system(cmd)
        except Exception as e:
            print(e)
        print("Conversion of projections done")

    def run_dark(self):
        if self.dark == "":
            return
        self.dark = self.dark[0]
        dataset = self.dark + "/measurement/" + self.cameratype
        print("Conversion of darks in progress...")
        data = EdfFrom3d(
            self.dark_name,
            dataset,
            acq_frame=self.acq_frame,
            stem="dark",
            digits=self.digits,
        )
        self.dump_files(data)
        cmd = (
            "mv "
            + self.dataset_output
            + "/dark"
            + "0" * self.digits
            + ".edf "
            + self.dataset_output
            + "/dark.edf"
        )
        os.system(cmd)
        print("Conversion of darks done")

    def run_flat(self):
        if len(self.flat) == 0:
            return
        dataset = "1.1/measurement/" + self.cameratype
        print("Conversion of flats in progress...")
        data = EdfFrom3d(
            self.flat_name,
            dataset,
            acq_frame=self.acq_frame,
            stem="ref",
            digits=self.digits,
        )
        self.dump_files(data)
        cmd = (
            "mv "
            + self.dataset_output
            + "/ref"
            + "0" * self.digits
            + ".edf "
            + self.dataset_output
            + "/refHST"
            + "0" * self.digits
            + ".edf"
        )
        os.system(cmd)

        try:
            cmd = (
                f"cp {self.dataset_output}/refHST"
                + "0" * self.digits
                + f".edf {self.dataset_output}/refHST{self.ref_on:0{self.digits}d}.edf"
            )
            print(cmd)
            os.system(cmd)
        except Exception as e:
            print(
                f"You might need to create {self.dataset_output}/{self.dataset}_{self.ref_on}.edf and {self.dataset_output}/refHST{self.ref_on:0{self.digits}d}.edf"
            )
            print(e)

    def run_static(self):
        if len(self.static) == 0:
            return
        self.static = self.static[0]
        dataset = self.dic_h5[self.static] + "/measurement/" + self.cameratype
        print("Conversion of end images in progress...")
        data = EdfFrom3d(
            self.h5_name,
            dataset,
            acq_frame=self.acq_frame,
            stem="static" + self.dataset,
            digits=self.digits,
            tomo_n=self.ref_on,
        )
        self.dump_files(data)
        # cmd = "mv " + self.dataset_output + "/static" + "0" * self.digits + ".edf " + self.dataset_output + "/static.edf"
        # os.system(cmd)
        print("Conversion of end images done")

    def finish(self):
        cmd = f"chmod -R 777 {self.dataset_output}"
        os.system(cmd)

    def execute(self, dark=True, flat=True, info=True):
        self.create_directory()
        self.run_projection()
        self.srot_position()
        self.run_static()
        if dark:
            self.run_dark()
        if flat:
            self.run_flat()
        if info:
            self.create_info()
        self.finish()


class EdfFrom3d(object):
    """Maps a 3D array in a hdf5 file to stack of 2D image files"""

    extn = ".edf"

    def __init__(
        self,
        h5filename,
        dataset,
        scan_time=None,
        current=None,
        time=None,
        stem="data",
        digits=4,
        tomo_n=0,
        **kwds,
    ):
        """
        h5filename = h5file to get the data from
        dataset = 3d array to map
        stem = output name stem
        """
        self.stem = stem
        self.h5o = h5py.File(h5filename, "r")
        self.data = self.h5o[dataset]
        self.current = None
        self.sx = None
        self.sy = None
        self.sz = None
        self.tomo_n = tomo_n

        self.fmt = f"%s%0{digits}d%s"
        self.dmt = f"%s_%0{digits}d%s"

        setattr(self, "acq_frame", kwds["acq_frame"])
        if self.stem == "dark":
            self.filename_list = [self.name(0)]
            self.filename_lut = {self.name(0): 0}
            self.data = np.array([np.mean(self.data, axis=0)], dtype="intc")

        elif self.stem == "ref":
            self.filename_list = [self.name(0)]
            self.filename_lut = {self.name(0): 0}
            self.data = np.array([np.median(self.data, axis=0)], dtype="intc")

        elif "static" in self.stem:
            self.stem = self.stem.replace("static", "")
            self.filename_list = [self.rename_static(i) for i in range(len(self))]
            self.filename_lut = {fname: i for i, fname in enumerate(self.filename_list)}
            self.filename_lut = {fname: i for i, fname in enumerate(self.filename_list)}
            self.filenames = set(self.filename_list)
            self.data = np.array(self.data / self.acq_frame, dtype=np.uint16)

        else:
            self.current = {}
            j = 0
            for i in range(len(scan_time)):
                while scan_time[i] > time[j] and j < len(time) - 1:
                    j += 1
                self.current[i] = current[j]

            assert len(self.data.shape) == 3, "We need a 3D array please!"
            # Decide on which frame has which filename:
            self.filename_list = [self.rename(i) for i in range(len(self))]
            self.filename_lut = {fname: i for i, fname in enumerate(self.filename_list)}
            self.filenames = set(self.filename_list)
            for key in kwds.keys():
                setattr(self, key, kwds[key])

        try:
            # data = np.array([], dtype=np.uint16)
            # for i in self.data:
            #    new = np.array(i / self.acq_frame, dtype=np.uint16)
            #    data = np.append(data, new)
            self.data = np.array(self.data / self.acq_frame, dtype=np.uint16)
            # self.data = data
        except:
            pass
        self._file_size = None

    def name(self, i):  # to override
        """Generate some filename pattern"""
        return self.fmt % (self.stem, i, self.extn)

    def rename(self, i):  # to override
        """Generate some filename pattern"""
        return self.dmt % (self.stem, i, self.extn)

    def rename_static(self, i):  # to override
        """Generate some filename pattern"""
        j = int(self.tomo_n) + i + 1
        return self.dmt % (self.stem, j, self.extn)

    def num(self, name):  # to override
        """Get the frame index from the filenane"""
        return self.filename_lut[name]

    def toBlob(self, i):
        """Convert the numpy array to a file"""

        try:
            edf = fabio.edfimage.edfimage(self.data[i])
            edf._frames[0]._index = 0  # strange that we need to do this?

            if self.current:
                edf.header["SRCUR"] = str(self.current[i])
            if self.sx and self.sy and self.sz:
                motor_mne = []
                motor_pos = []
                if self.sx in self.h5o:
                    motor_mne.append("sx")
                    motor_pos.append(str(self.h5o[self.sx][()]))
                if self.sy in self.h5o:
                    motor_mne.append("sy")
                    motor_pos.append(str(self.h5o[self.sy][()]))
                if self.sz in self.h5o:
                    motor_mne.append("sz")
                    if "positioners" in self.sz:
                        motor_pos.append(str(self.h5o[self.sz][()]))
                    else:
                        motor_pos.append(str(self.h5o[self.sz][()][i]))
                edf.header["motor_mne"] = " ".join(motor_mne)
                edf.header["motor_pos"] = " ".join(motor_pos)
            blob = bytearray(edf._frames[0].get_edf_block())
        except Exception as e:
            print(e)
        finally:
            edf.close()
        return blob

    def filesize(self, arg=0):  # to override
        """Size of the files"""
        if self._file_size is None:
            blob = self[arg]
            self._file_size = len(blob)  # getbuffer().nbytes
        return self._file_size

    # The rest is hopefully common to most 3D data arrays
    #  ... changes if you piece together scans in a h5 etc
    def __len__(self):
        """Number of frames"""
        return self.data.shape[0]

    @functools.lru_cache(maxsize=LRU_CACHE_SIZE)  #
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


def makeargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("h5_names")
    parser.add_argument("edf_directory")
    # parser.add_argument('--start_nb', dest="start_nb", default=1)
    parser.add_argument("--report", dest="report", default="False")
    parser.add_argument(
        "--dark",
        dest="dark",
        default="True",
        help="If the h5 contains darks, True by default",
    )
    parser.add_argument(
        "--flat",
        dest="flat",
        default="True",
        help="If the h5 contains flats, True by default",
    )
    return parser


if __name__ == "__main__":
    # h5_names = '/data/visitor/md1290/bm18/HA-900_6.54um_LADAF-2021-17_heart_ROI-01_0000*'
    # edf_directory = '/data/visitor/md1290/EDF/test'
    # args="'/data/visitor/md1290/bm18/HA-900_6.54um_LADAF-2021-17_heart_ROI-01_0000*' '/data/visitor/md1290/EDF/test'"

    parser = makeargs()
    args = parser.parse_args()
    if "*" not in args.h5_names:
        if args.h5_names[-3:] != ".h5":
            if args.h5_names[-1] == "/":
                args.h5_names = args.h5_names[:-1]
            args.h5_names += "*"
        else:
            h5_names = [args.h5_names]
    else:
        h5_names = [args.h5_names]
    if "*" in args.h5_names:
        h5_names = []
        for i in glob(args.h5_names):
            for j in glob(i + "/*.h5"):
                if "tomwer" not in j and "nabu" not in j:
                    h5_names.append(j)
        h5_names.sort()

    edf_directory = args.edf_directory
    # start_nb = args.start_nb
    if not os.path.exists(edf_directory):
        os.system(f"mkdir {edf_directory}")

    for h5_name in h5_names:
        if "flat" in h5_name:
            continue
        print(h5_name)
        directory = os.path.dirname(h5_name)
        dataset = directory.split("/")[-1]
        dataset_output = os.path.join(edf_directory, dataset + "_")
        rights = os.popen(f"ls -l {dataset_output}").read()
        rights = rights.split("\n")
        processed = False
        for right in rights:
            if dataset in right and "rwxrwxrwx" in right:
                processed = True
        if processed:
            # Check if correct number of files
            # Check if right size of files
            print("Already converted")
            continue
        h5 = H5Handler(h5_name, edf_directory)
        if "fast_acq" not in dir(h5) and "end_time" not in dir(h5):
            continue
        if args.report is True:
            print(h5.create_report())
        else:
            h5.execute(dark=args.dark, flat=args.flat)
