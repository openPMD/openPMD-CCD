"""
This test file is part of the openPMD-CCD.

Copyright 2020 openPMD contributors
Authors: Axel Huebl
License: BSD-3-Clause-LBNL
"""
from PIL import Image
import io
import numpy as np
import os
import pytest

from openpmd_ccd import CCD


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
)

@pytest.mark.datafiles(FIXTURE_DIR)
def test_write(datafiles):
    """ test writes from the README """

    scan = CCD("defaultCam_scan001.h5", overwrite=True,
               name="Go Pro", model="HERO8 Black", serial="12345678",
               operator="Axel Huebl <axelhuebl@lbl.gov>",
               # resolution=None, roi=None, exposure_time=None
    )

    image_path = str(datafiles.listdir()[0])

    # add by bytes
    with io.BytesIO() as image_data:
        im = Image.open(image_path)
        im.save(image_data, im.format)
        image_data.seek(0)
        im_numpy = np.array(im)
        for image_number in range(10):
            scan.add(image_number, image_data=im)
        for image_number in range(10, 20):
            scan.add(image_number, image_data=image_data)
        for image_number in range(30, 40):
            scan.add(image_number, image_data=im_numpy)

    # add by list of list of uints (LabView)
    im_list = [[1, 2, 3], [4, 5, 6]]
    for image_number in range(40, 50):
        scan.add(image_number, image_data=im_list)

    # add by path
    for image_number in range(50, 60):
        scan.add(image_number, image_path)
    
    # scan.recalibrate(...)

    scan.close()
    del scan
