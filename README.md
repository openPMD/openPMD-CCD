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

For using this with LabView (2020 or newer), create a ``openpmd_ccd_labview.py`` [wrapper file](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019UFmSAM&l=en-US) and [populate it with the following content (link)](openpmd_ccd_labview.py?raw=1).

You have to **name your CCDs uniquely**.

You can now call the ``open_write``, ``add``, ``recalibrate`` and ``close`` functions with their respective parameters.

General latency estimate when [starting python scripts from LabView](https://zone.ni.com/reference/en-XX/help/371361R-01/glang/python_node/) (measured on a regular Windows PC in 2020):

- Session startup: ~250ms
- First function call into a module: ~1-2ms (simple `numpy` and `h5py` load)
- Further function calls: ~0.3ms

There are three modes to pass an image, exemplified with a 2250x2250 pixel image matrix (16bit depth):
- as numpy array (`image_data` as `numpy.ndarray`):
  - passing to Python: ~20-23ms
- as a list (`image_data` as `list`):
  - passing to Python: ~300ms [(implicit list conversion)](https://twitter.com/axccl/status/1257537488148520962)
  - converting list back to numpy: ~700ms
- via a file path (`image_path` as `string`):
  - overall: 100s of ms and more

The write of the actual data to HDF5 (`add()` call) in the given example takes about 9.1ms per image.
All above values will change depending on Python installation, loaded modules and computer hardware (mainly memory and CPU).

Please see the [example.vi](labview/example.vi) file:

[![LabView example](labview/preview.png)](labview/example.vi)


## Author Contributions

- [Axel Huebl (LBNL)](https://github.com/ax3l): implementation
- [Anthony Gonsalves (LBNL)](https://atap.lbl.gov/division-leadership/atap-scientific-staff/): consulting and LabView integration

### Transitive Contributions

- [ADIOS](https://github.com/ornladios/ADIOS2) by [S. Klasky (ORNL), team, collaborators](https://csmd.ornl.gov/adios) and [contributors](https://github.com/ornladios/ADIOS2/graphs/contributors) (planned)
- [Blosc](https://blosc.org) by [Francesc Alted](https://github.com/FrancescAlted) and [contributors](https://github.com/Blosc/c-blosc/graphs/contributors) (planned)
- HDF5 by [the HDF group](https://www.hdfgroup.org/) and community
- the [openPMD-standard](https://github.com/openPMD/openPMD-standard) by Axel Huebl (HZDR, now LBNL) and contributors
