"""
This test file is part of the openPMD-CCD.

Copyright 2020 openPMD contributors
Authors: Axel Huebl
License: 3-Clause-BSD-LBNL
"""
from dateutil.tz import tzlocal
from pathlib import Path
from PIL import Image
import datetime
import h5py as h5
import io
import numpy as np
import os
import socket
import sys

# from profilehooks import profile

from .__version__ import __version__


class CCD(object):
    def __init__(self, file_path, overwrite=False,
                 name=None, model=None, serial=None, operator=None,
                 resolution=None, roi=None, exposure_time=None,
                 swmr=True
                ):
        """
        Open the CCD data series.

        Parameters
        ----------
        file_path: string
            The path to a series to be created created
        overwrite: bool, optional
            If set to True, this will silently overwrite existing files.

        name: string, optional
            Camera name in a setup.
        model: string, optional
            Camera model.
        serial: string, optional
            Camera serial number.
        operator: string, optional
            Operator/author taking the images.
            Format is "First Last <e-mail>" (comma separated for multiple).

        resolution: list of two floats (x, y), optional
            Spatial resolution of the camera in meters.
        roi: list of four floats, optional
            FIXME ? Position in x, position in y, height, width (unit? x=w, y=h?)
        exposure_time: float, optional
            FIXME ? Exposure time in seconds.

        swmr: boolean, optional
            Single-Writer-Multi-Reader (SWMR) support in HDF5.
            Keep this enabled unless it does not work. This is a HDF5 1.10+
            feature on POSIX platforms (Linux, macOS, Windows on Cygwin) that
            makes sure that open files are always in a consistent, readable
            state - even if an application crashes.
            https://support.hdfgroup.org/HDF5/docNewFeatures/NewFeaturesSwmrDocs.html
        """
        # sanitize file path: spaces to _ and crop to 255 in file name
        input_filepath = Path(file_path)
        head_tail = os.path.split(input_filepath)
        print(head_tail)
        head_tail_san = head_tail[1].replace(" ", "_")  # spaces to underscores
        head_tail_san = head_tail[1][:255]              # windows limit anyway
        file_path = os.path.join(head_tail[0], head_tail_san)

        if not overwrite:
            assert not os.path.isfile(file_path), (
                "[openPMD-CCD] File '{0}' already exists!".format(file_path) )

        self._mode = "write"
        if name is None:
            name = "unknown"
        self._name = name
        if model is None:
            model = "unknown"
        self._model = model
        if serial is None:
            serial = "unknown"
        self._serial = serial
        if operator is None:
            operator = "unknown"
        self._operator = operator
        if resolution is None:
            resolution = [1.0, 1.0]
        self._resolution = resolution
        if roi is None:
            roi = [0., 0., 1., 1.]
        self._roi = roi
        if exposure_time is None:
            exposure_time = "unknown"
        self._exposure_time = exposure_time
        self._f = h5.File(file_path, 'w', swmr=swmr)

        def get_software_dependencies():
            """
            Returns the software dependencies of this script as a semicolon
            separated string.
            """
            return np.string_(
                "python@{0}.{1}.{2};".format(
                    sys.version_info.major,
                    sys.version_info.minor,
                    sys.version_info.micro
                ) +
                "numpy@{0};".format( np.__version__ ) +
                "pillow@{0};".format( Image.__version__ ) +
                "hdf5@{0};".format( h5.version.hdf5_version ) +
                "h5py@{0}".format( h5.__version__)
            )

        # openPMD attributes
        self._f.attrs["openPMD"] = np.string_("1.1.0")
        self._f.attrs["openPMDextension"] = np.uint32(0)

        self._f.attrs["basePath"] = np.string_("/data/%T/")
        self._f.attrs["meshesPath"] = np.string_("shots/")
        self._f.attrs["iterationEncoding"] = np.string_("groupBased")
        self._f.attrs["iterationFormat"] = np.string_("/data/%T/")

        if self._operator is not None:
            self._f.attrs["author"] = np.string_(self._operator)
        self._f.attrs["software"] = np.string_("openPMD-CCD")
        self._f.attrs["softwareVersion"] = np.string_(__version__)
        self._f.attrs["softwareDependencies"] = get_software_dependencies()
        self._f.attrs["machine"] = np.string_(socket.gethostname())
        self._f.attrs["date"] = np.string_(
            datetime.datetime.now(tzlocal()).strftime('%Y-%m-%d %H:%M:%S %z'))

        self._f.create_group("data")

        # CCD specific attributes
        self._f.attrs["ccdName"] = self._name
        self._f.attrs["ccdModel"] = self._model
        self._f.attrs["ccdSerial"] = self._serial


    def recalibrate(self, resolution=None, roi=None, exposure_time=None):
        """
        Change calibration parameters

        Parameters
        ----------
        resolution: list of two floats (x, y)
            Spatial resolution of the camera in meters.
        roi: list of four floats
            FIXME ? Position in x, position in y, height, width (unit? x=w, y=h?)
        exposure_time: float
            FIXME ? Exposure time in seconds.
        """
        assert self._mode == "write", (
            "[openPMD-CCD] Recalibration is only possible in write mode.")

        if resolution is not None:
            self._resolution = resolution
        if roi is not None:
            self._roi = roi
        if exposure_time is not None:
            self._exposure_time = exposure_time


    # @profile
    def add(self, image_number, image_path=None, image_data=None):
        """
        Add a new image.

        Parameters
        ----------
        image_number: integer
            Shot or image number in a data series.
        image_path: path to an image
            Provide this to pass an image from disk.
        image_data: image data as numpy.ndarray, PIL.image, or io.BytesIO image
            ndarray or image
        """
        assert self._mode == "write", (
            "[openPMD-CCD] Adding an image is only possible in write mode.")
        assert image_path is not None or image_data is not None, (
            "[openPMD-CCD] Either an image file or an image path is needed.")
        # TODO: check if image_number exists??

        im_numpy = None
        if image_path is not None:
            im = Image.open(image_path)          # >60ms/image (cached?): load from file to PIL.Image
        if image_data is not None:
            if issubclass(type(image_data), Image.Image):
                im = image_data                  # negligible: already an PIL.Image
            elif issubclass(type(image_data), np.ndarray):
                im_numpy = image_data            # negligible: already a numpy array
            else:
                im = Image.open(image_data)      # ~54ms/image: mem-bytes to PIL.Image

        if im_numpy is None:
            # im.load()                          # PIL.Image.open are lazy operations
            im_numpy = np.array(im)              # ~21ms/image: PIL.Image to numpy

        # ~9.1ms/image
        compression = None
        compression_opts = None
        im_h5 = self._f.create_dataset("data/{:06}/shots/raw".format(image_number),
                                       data=im_numpy, compression=compression,
                                       compression_opts=compression_opts)

        # openPMD attributes (negligible time)
        base_dir = self._f["data/{:06}".format(image_number)]
        base_dir.attrs["time"] = datetime.datetime.utcnow().timestamp()
        base_dir.attrs["dt"] = 0.0   # unused
        base_dir.attrs["timeUnitSI"] = np.float64(1.0) # unused

        im_h5.attrs["geometry"] = np.string_("cartesian")
        im_h5.attrs["gridSpacing"] = np.array(self._resolution, dtype=np.float64)   # dx, dy
        im_h5.attrs["gridGlobalOffset"] = np.array(self._roi[0:2], dtype=np.float64)
        im_h5.attrs["gridUnitSI"] = np.float64(1.0)  # already in meters
        im_h5.attrs["position"] = np.array([0.0, 0.0], dtype=np.float32)  # unused FIXME?
        im_h5.attrs["dataOrder"] = np.string_("C")
        im_h5.attrs["timeOffset"] = 0.0  # Time offset with basePath's time
        im_h5.attrs["axisLabels"] = np.array([b"x", b"y"])
        im_h5.attrs["unitSI"] = 1.0  # unknown FIXME?
        im_h5.attrs["unitDimension"] = \
           np.array([0.0, 1.0, -2.0, 0.0, 0.0, 0.0, 0.0 ], dtype=np.float64)
           #          L    M     T    I  theta  N    J
           # Fluence is radiant energy per surface area

        # CCD specific attributes
        im_h5.attrs["ccdResolution"] = self._resolution
        im_h5.attrs["ccdROI"] = self._roi
        im_h5.attrs["ccdROILabels"] = np.array([b"x", b"y", b"w", b"h"])
        im_h5.attrs["ccdExposureTime"] = self._exposure_time


    def close(self):
        """ Close the CCD data series. """
        self._f.close()
        del self._f
        self._f = None
        self._mode = "closed"
