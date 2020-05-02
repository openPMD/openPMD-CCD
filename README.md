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

For LabView usage, create a ``openpmd_ccd.py`` [wrapper file](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019UFmSAM&l=en-US) and populate it with:
```py
from openpmd_ccd import CCD

scan = dict()  # scan series per camera name (global state per session)


# FIXME: add prefix path? add scan number?
def open_write(name, model=None, serial=None, operator=None, resolution=None, roi=None, exposure_time=None):
    assert not key in scan, "[openPMD-CCD] You cannot define the same CCD name twice."

    scan[name] = CCD(
        "ccd_{0}.h5".format(name),
        False,
        name, model, serial, operator,
        resolution, roi, exposure_time)


def add(name, image_number, image_path=None, image_data=None):
    assert key in scan, "[openPMD-CCD] CCD name not known (open_write called?)."
    scan.add(name, image_number, image_path, image_data)


def recalibrate(name, resolution=None, roi=None, exposure_time=None):
    assert key in scan, "[openPMD-CCD] CCD name not known (open_write called?)."
    scan[name].recalibrate(name, resolution, roi, exposure_time)


def close(name):
    assert name in scan, "[openPMD-CCD] CCD name not known (open_write called?)."
    scan[name].close()
    del scan[name]
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
