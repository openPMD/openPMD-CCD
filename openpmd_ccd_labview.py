#!/usr/bin/env python
#
from openpmd_ccd import CCD
import os


# Start Configuration #########################################################
config_allow_overwrite = False  # Overwrite scan data if filename exists?
config_create_directory = True  # Create directory if it does not exist yet?
# End Configuration ###########################################################

# scan series per camera name (global state per LavView Python session)
scan = dict()

# cluster
# Ref.:
#   https://zone.ni.com/reference/en-XX/help/371361R-01/lvconcepts/using_standard_error_in/
#   https://zone.ni.com/reference/en-XX/help/371361R-01/lvconcepts/using_standard_error_out/
#   https://zone.ni.com/reference/en-XX/help/371361R-01/glang/python_node/
#   https://forums.ni.com/t5/LabVIEW/LabVIEW-cluster-and-python-node/td-p/3846386
# 	"cluster[0] -> Integer, cluster[1] -> String, cluster[2] -> Integer"
# success: (False, 0, "source name")
# warning: (False, 42, "source name")
# error:   (True, 42, "source name")


def open_write(directory_path, ccd_name, scan_number=None, ccd_model=None,
               ccd_serial=None, ccd_operator=None, ccd_resolution=None,
               ccd_roi=None, ccd_exposure_time=None):
    """ FIXME: doc strings """
    assert not ccd_name in scan, "[openPMD-CCD] You cannot define the same CCD name twice."

    if scan_number is not None:
        file_name = "{0}_scan_{0}_ccd.h5".format(ccd_name, scan_number)
    else:
        file_name = "{0}_ccd.h5".format(ccd_name)
    file_path = os.path.join(directory_path, file_name)

    #... dir name ...
    #if config_create_directory:
    #    ...

    scan[ccd_name] = CCD(
        file_path,
        config_allow_overwrite, config_create_directory,
        ccd_name, ccd_model, ccd_serial, ccd_operator,
        ccd_resolution, ccd_roi, ccd_exposure_time)
    # FIXME: try-catch and return status "cluster" (tuple)


def add(ccd_name, image_number, image_data=None, image_path=None):
    """ FIXME: doc strings """
    assert ccd_name in scan, "[openPMD-CCD] CCD name not known (open_write called?)."
    scan[ccd_name].add(image_number, image_data=image_data, image_path=image_path)
    # FIXME: try-catch and return status "cluster" (tuple)


def recalibrate(ccd_name, resolution=None, roi=None, exposure_time=None):
    """ FIXME: doc strings """
    assert ccd_name in scan, "[openPMD-CCD] CCD name not known (open_write called?)."
    scan[ccd_name].recalibrate(resolution, roi, exposure_time)
    # FIXME: try-catch and return status "cluster" (tuple)


def close(ccd_name):
    """ FIXME: doc strings """
    assert ccd_name in scan, "[openPMD-CCD] CCD name not known (open_write called?)."
    scan[ccd_name].close()
    del scan[ccd_name]
    # FIXME: try-catch and return status "cluster" (tuple)


if __name__ == "__main__":
    open_write("./", "defaultCam")
    add("defaultCam", 0, [[1, 2, 3], [4, 5, 6]])
    add("defaultCam", 1, [[3, 4, 5], [6, 7, 8]])
    add("defaultCam", 2, [[6, 7, 8], [9, 0, 1]])
    close("defaultCam")
