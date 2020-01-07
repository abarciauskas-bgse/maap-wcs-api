# MAAP WCS API

Prototype of OGC Coverages (WCS) API leveraging MAAP CMR.

Right now just implements the rangeset endpoint for tif files.

- Queries CMR for all granules within the collection that overlap with the bounding box parameter
- Merges files (limited to first 2 granules for now for performance reasons)
- Clips merged
- returns data as multi-dimensional `dataBlock`

## Creating / Installing Conda Environment

```
git clone git@github.com:abarciauskas-bgse/maap-wcs-api.git
cd maap-wcs-api
conda env create maap-wcs-api -f environment.yml
conda activate maap-wcs-api
export FLASK_APP=flaskapp
export FLASK_ENV=development
flask run
```

## Example requests

```
http://35.168.23.55:5000/collections/AfriSAR_UAVSAR_Coreg_SLC/coverage/rangeset?bounding_box=11.62,-0.05,11.64,-0.04
http://35.168.23.55:5000/collections/AFLVIS2/coverage/rangeset?bounding_box=10,-0.5,11,0
```

!(screenshot)[Screen Shot 2020-01-07 at 3.52.45 PM.png]
