"""
SkylabStudio - Python Client
For more information, visit https://studio.skylabtech.ai
"""

import json
import logging
import requests
import os
import time

from .version import VERSION

API_HEADER_KEY = 'X-SLT-API-KEY'
API_HEADER_CLIENT = 'X-SLT-API-CLIENT'

LOGGER = logging.getLogger('skylab_studio')
LOGGER.propagate = False

class api: #pylint: disable=invalid-name
    """
    The client for accessing the Skylab Studio platform.

    Args:
        api_key (str): Your account's API KEY.

    Attributes:
        api_proto (str): The API endpoint protocol.
        api_port (str): The API endpoint port.
        api_host (str): The API endpoint host name.
        api_version (str): The API endpoint version number.
        api_key (str): The API key to use.
        debug (boolean): Whether or not to allow debugging information to be printed.
        hmac (boolean): Whether or not to use hmac authentication
    """

    # staging
    # api_proto = 'https'
    # api_port = '443'
    # api_host = 'studio-staging.skylabtech.ai'

    # development
    api_proto = 'http'
    api_port = '3000'
    api_host = 'localhost'

    api_version = '1'
    api_key = 'THIS_IS_A_TEST_API_KEY'

    debug = False
    hmac = False

    def __init__(self, api_key=None, **kwargs):
        print('kwargs', kwargs)
        if not api_key:
            raise Exception("You must specify an api key")

        self.api_key = api_key

        if 'api_host' in kwargs:
            self.api_host = kwargs['api_host']
        if 'api_proto' in kwargs:
            self.api_proto = kwargs['api_proto']
        if 'api_port' in kwargs:
            self.api_port = kwargs['api_port']
        if 'api_version' in kwargs:
            self.api_version = kwargs['api_version']
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        if 'hmac' in kwargs:
            self.hmac = kwargs['hmac']

        if self.debug:
            logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)

            LOGGER.debug('Debug enabled')
            LOGGER.propagate = True

    def _build_http_auth(self):
        return (self.api_key, '')

    # @staticmethod
    def _build_request_headers(self):
        client_header = '%s-%s' % (
            'python',
            VERSION
        )

        headers = {
            API_HEADER_CLIENT: client_header,
            'X-SLT-API-KEY': self.api_key,
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

        return headers

    def _build_request_path(self, endpoint):
        path = '/api/public/v%s/%s' % (self.api_version, endpoint)

        path = "%s://%s:%s%s" % (
            self.api_proto,
            self.api_host,
            self.api_port,
            path
        )

        return path

    @staticmethod
    def _build_payload(data):
        if not data:
            return None

        return json.dumps(data)

    def _api_request(self, endpoint, http_method, **kwargs):
        """Private method for api requests"""
        LOGGER.debug(' > Sending API request to endpoint: %s', endpoint)

        headers = self._build_request_headers()
        LOGGER.debug('\theaders: %s', headers)

        path = self._build_request_path(endpoint)
        LOGGER.debug('\tpath: %s', path)

        data = self._build_payload(kwargs.get('payload'))
        if not data:
            data = kwargs.get('data')
        LOGGER.debug('\tdata: %s', data)

        req_kw = dict(
            headers=headers,
        )

        if http_method == 'POST':
            if data:
                response = requests.post(path, data=data, **req_kw)
            else:
                response = requests.post(path, **req_kw)
        elif http_method == 'PUT':
            response = requests.put(path, data=data, **req_kw)
        elif http_method == 'DELETE':
            response = requests.delete(path, **req_kw)
        else:
            response = requests.get(path, data=data, **req_kw)

        LOGGER.debug('\tresponse code:%s', response.status_code)

        try:
            LOGGER.debug('\tresponse: %s', response.json())
        except ValueError:
            LOGGER.debug('\tresponse: %s', response.content)

        return response

    def list_jobs(self):
        """ API call to get all jobs """
        return self._api_request(
            'jobs',
            'GET'
        )

    def create_job(self, payload=None):
        """ API call to create a job """
        return self._api_request(
            'jobs',
            'POST',
            payload=payload
        )

    def get_job(self, job_id):
        """ API call to get a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'GET'
        )

    def get_job_by_name(self, payload=None):
        return self._api_request(
            'jobs/find_by_name',
            'GET',
            payload=payload
        )

    def update_job(self, job_id, payload=None):
        """ API call to update a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'PUT',
            payload=payload
        )
    
    def update_job_callback_url(self):
        return self._api_request(
            'jobs/job_callback_url',
            'PATCH'
        )

    def queue_job(self, job_id, payload=None):
        return self._api_request(
            'jobs/%s/queue' % job_id,
            'POST',
            payload=payload
        )
    
    def fetch_jobs_in_front(self, job_id):
        return self._api_request(
            'jobs/%s/jobs_in_front' % job_id,
            'GET',
        )

    def delete_job(self, job_id):
        """ API call to delete a specific job """
        return self._api_request(
            'jobs/%s' % job_id,
            'DELETE'
        )

    def process_job(self, job_id):
        """ API call to process a specific job """
        return self._api_request(
            'jobs/%s/process' % job_id,
            'POST'
        )

    def cancel_job(self, job_id):
        """ API call to cancel a specific job """
        return self._api_request(
            'jobs/%s/cancel' % job_id,
            'POST'
        )

    def list_profiles(self):
        """ API call to get all profiles """
        return self._api_request(
            'profiles',
            'GET'
        )

    def create_profile(self, payload=None):
        """ API call to create a profile """
        return self._api_request(
            'profiles',
            'POST',
            payload=payload
        )

    def get_profile(self, profile_id):
        """ API call to get a specific profile """
        return self._api_request(
            'profiles/%s' % profile_id,
            'GET'
        )

    def update_profile(self, profile_id, payload=None):
        """ API call to update a specific profile """
        return self._api_request(
            'profiles/%s' % profile_id,
            'PUT',
            payload=payload
        )

    def list_photos(self):
        """ API call to get all photos """
        return self._api_request(
            'photos',
            'GET'
        )

    def create_photo(self, payload=None):
        """ API call to create a photo """
        return self._api_request(
            'photos',
            'POST',
            payload=payload
        )

    def upload_photo(self, photo_path, model, id, skip_cache=False):

        photo_name = os.path.basename(photo_path)
        # create photo
        # upload retry w/ backoff
        # handle upload error

        # Read file contents to binary
        data = open(photo_path, "rb")

        # model - either job or profile (job_id/profile_id)
        photo_data = { f"{model}_id": id, "name": photo_name }

        if skip_cache and model == 'job':

          photo_data['skip_cache'] = skip_cache

          # Ask studio to create the photo record
          photo_resp = self.create_photo(photo_data)
          core_job_id = photo_resp.json()['coreJobId']

          payload = {
              "skip_cache": skip_cache,
              "job_id": id,
              "photo_name": photo_name,
              "core_job_id": core_job_id
          }

          # Ask studio for a presigned url
          upload_url_resp = self._api_request('photos/upload_url', 'GET', payload=payload)
          upload_url = upload_url_resp.json()['url']
        else:
          # Ask studio for a presigned url + key
          upload_url_resp = self._api_request('photos/upload_url', 'GET')
          key = upload_url_resp.json()['key']
          upload_url = upload_url_resp.json()['url']

          if not key:
            raise Exception('Unable to obtain upload key')

          if not upload_url:
            raise Exception('Unable to obtain upload_url')

          photo_data['key'] = key

          self.create_photo(photo_data)

        # PUT request to presigned url with image data
        upload_photo_resp = requests.put(upload_url, data)

        if upload_photo_resp.status_code is not 200:
          retry = 0
          # retry upload
          while retry < 3:
            upload_photo_resp = requests.put(upload_url, data)
            if upload_photo_resp.status_code is not 200:
                if retry == 2:  # Check if retry count is 2 (0-based indexing):
                    raise Exception('Unable to upload to bucket after retrying.')

                time.sleep(1)
                retry += 1

        return upload_photo_resp


    def get_photo(self, photo_id):
        """ API call to get a specific photo """
        return self._api_request(
            'photos/%s' % photo_id,
            'GET'
        )

    def get_job_photos(self, job_identifier, value):
        """
          job identifier - either id or name
          value - the actual job_id or job_name
        """
        payload = {
            f"job_{job_identifier}": value
        }
        return self._api_request(
            'photos/list_for_job',
            'GET',
            payload=payload
        )

    def update_photo(self, photo_id, payload=None):
        """ API call to update a specific photo """
        return self._api_request(
            'photos/%s' % photo_id,
            'PUT',
            payload=payload
        )

    def delete_photo(self, photo_id):
        """ API call to delete a specific photo """
        return self._api_request(
            'photos/%s' % photo_id,
            'DELETE'
        )
