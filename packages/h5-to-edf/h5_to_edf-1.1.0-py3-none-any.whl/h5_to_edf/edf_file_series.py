# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2015-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import os
import numpy
import fabio
import pathlib


class EdfFileSeries:
    """File series based on EDF.

    This only support writing of file series.

    Arguments:
        output_directory: Directory used to write the file series
        filename_pattern: Filename pattern with escape `{index}` to locallise the file index
        dry_run: Set to true to disable any IO operation
    """

    def __init__(
        self,
        output_directory: str | pathlib.Path,
        filename_pattern: str,
        dry_run: bool = False,
        first_index=0,
    ):
        self._output_directory: str = str(output_directory)
        self._filename_pattern: str = filename_pattern
        self._dry_run: bool = dry_run
        self._first_index = first_index
        self._index = first_index
        self._closed = False

    def __enter__(self):
        self._raiseIfClosed()
        if self._index != self._first_index:
            raise RuntimeError("File series was already open/closed")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def append(self, data: numpy.ndarray, header: dict):
        self._raiseIfClosed()
        try:
            filename = self._filename_pattern.format(index=self._index)
            path = os.path.join(self._output_directory, filename)
            edf = fabio.edfimage.edfimage(data=data, header=header)
            if not self._dry_run:
                edf.save(path)
        finally:
            self._index += 1

    def flush(self):
        """Flush the file with the last data received."""
        self._raiseIfClosed()

    def close(self):
        self._raiseIfClosed()
        self._closed = True

    def _raiseIfClosed(self):
        if self._closed:
            raise RuntimeError("File series was closed")
