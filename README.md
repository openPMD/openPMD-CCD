# openPMD-CCD

A Small Python Module to Write CCD Images to openPMD.

License: TBD, likely BSD-3-Clause-LBNL


## Install

```bash
# optional:            --user
python3 -m pip install        git+https://github.com/ax3l/openPMD-CCD.git
```


## Usage (Write)

### Python

Generally, you can use this as follows:
```py
from openpmd_ccd import CCD

scan = CCD("defaultCam_scan001.h5", overwrite=True,
           name="Go Pro", model="HERO8 Black", serial="12345678",
           operator="Axel Huebl <axelhuebl@lbl.gov>",
           # resolution=None, roi=None, exposure_time=None
)

scan.add(0, "tests/data/Scan005_SimCam_001.png")
scan.add(1, np.array([[1., 2.], [3., 4.]]))

# scan.recalibrate(...)

scan.close()
```

### LabView

For using this with LabView (2018 or newer), create a ``openpmd_ccd_labview.py`` [wrapper file](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019UFmSAM&l=en-US) and [populate it with](openpmd_ccd_labview.py):
```py
from openpmd_ccd import CCD
import os


# Start Configuration #########################################################
config_allow_overwrite = False  # Overwrite scan data if filename exists?
config_create_directory = True  # Create directory if it does not exist yet?
# End Configuration ###########################################################

# scan series per camera name (global state per LavView Python session)
scan = dict()

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
```

You have to **name your CCDs uniquely**.

You can now call the ``open_write``, ``add``, ``recalibrate`` and ``close`` functions with their respective parameters.

General latency estimate when [starting python scripts from LabView](https://zone.ni.com/reference/en-XX/help/371361R-01/glang/python_node/) (measured on a regular Windows PC in 2020):

- Session startup: ~250ms
- First function call into a module: ~1-2ms (simple `numpy` and `h5py` load)
- Further function calls: ~0.3ms

The above values will change depending on Python installation and loaded modules.


## Author Contributions

- [Axel Huebl (LBNL)](https://github.com/ax3l): implementation
- [Anthony Gonsalves (LBNL)](https://atap.lbl.gov/division-leadership/atap-scientific-staff/): consulting and LabView integration

### Transitive Contributions

- [ADIOS](https://github.com/ornladios/ADIOS2) by [S. Klasky (ORNL), team, collaborators](https://csmd.ornl.gov/adios) and [contributors](https://github.com/ornladios/ADIOS2/graphs/contributors) (planned)
- [Blosc](https://blosc.org) by [Francesc Alted](https://github.com/FrancescAlted) and [contributors](https://github.com/Blosc/c-blosc/graphs/contributors) (planned)
- HDF5 by [the HDF group](https://www.hdfgroup.org/) and community
- the [openPMD-standard](https://github.com/openPMD/openPMD-standard) by Axel Huebl (HZDR, now LBNL) and contributors
