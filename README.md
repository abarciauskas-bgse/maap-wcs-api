# MAAP WCS API

Prototype of OGC Coverages (WCS) API leveraging MAAP CMR.

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
http://localhost:5000/collections/AFLVIS2/coverage/rangeset?bounding_box=10,-0.5,11,0
```

