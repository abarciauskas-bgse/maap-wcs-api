import os
import requests
import subprocess
import xarray as xr
from dask.distributed import Client, LocalCluster
import rasterio
from flask import Flask, json, request

base_maap_url = 'https://cmr.maap-project.org/search'

def domain_set(event):
    """
    TODO
    """
    collectionid = event['pathParameters']['collectionid']
    collection_metadata_url = f"{base_maap_url}/collections.umm_json?short_name={collectionid}"
    headers = {'Echo-Token': os.getenv('CMR_TOKEN')}
    collection_metadata = requests.get(collection_metadata_url, headers=headers)
    return requests.get(collection_metadata).content

def subset(collectionid, bbox_params):
    bbox = bbox_params.replace(',', ' ')
    resp = requests.get(f"{base_maap_url}/granules.json?short_name={collectionid}&bounding_box={bbox_params}")
    granules = json.loads(resp.content)['feed']['entry']
    granules_urls = []
    for g in granules:
        browse_match = list(link for link in g['links'] if 'title' in link and link['title'] == '(BROWSE)')
        file_match = list(link for link in g['links'] if 'title' in link and link['title'] == 'File to download')
        if len(browse_match) == 1:
            file_url = browse_match[0]['href']
        elif len(file_match) == 1:
            file_url = file_match[0]['href']
        else:
            raise 'No file found'
        granules_urls.append(file_url.replace('s3://','/vsis3/'))

    # TEMPORARY: Limit merging to something
    granules_urls = granules_urls[0:2]
    subprocess.check_output(['rio','merge', *granules_urls, 'merged.tif', '--overwrite'])
    subprocess.check_output(['rio', 'clip', 'merged.tif', 'output.tif', '--bounds', bounds, '--overwrite'])
    # result = subprocess.check_output(['rio', 'info', 'output.tif', '--indent', '2', '--verbose'])
    data = rasterio.open('output.tif').read()
    return {
            'type': 'RangeSetType',
            'dataBlock': data.tolist()
            }

# should there be a good way to remove nodata value
event = {
    'resource': 'rangeset',
    'queryStringParameters': {
        'bounding_box': '9.1,0.4,9.8,0.6'
    },
    'pathParameters': {
        'collectionid': 'AFLVIS2'
    }
}
# print(lambda_handler(event, None))
# TODO:
# (other servers) Create CMR provider for pygeoapi
# (my server) Package + Deploymment to AWS
# Implement RangeSetRefType (for RangeSet response)
# Implement other endpoints

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/collections/<string:collectionid>/coverage/rangeset')
    def rangeset(collectionid):
        bbox = request.args.get('bounding_box')
        data = subset(collectionid, bbox)
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

    return app

