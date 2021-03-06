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

## Running on AWS EC2

* Launch and log in to Miniconda with Python 3(ami-062c42cbecc1d5ec0)
* `sudo yum install git -y`
* Export AWS credentials
* Run same commands as in section above for local install, git clone etc.
* Run in background

```
nohup flask run --host=0.0.0.0 > 1.txt 2>&1 &
```

## Example requests

```
http://35.168.23.55:5000/collections/AfriSAR_UAVSAR_Coreg_SLC/coverage/rangeset?bounding_box=11.62,-0.05,11.64,-0.04
http://35.168.23.55:5000/collections/AFLVIS2/coverage/rangeset?bounding_box=10,-0.5,11,0
```

![screenshot](./screenshot.png)
