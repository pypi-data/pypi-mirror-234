"""
Tests for SkylabStudio - Python Client
"""

import pytest
import requests_mock

import skylab_studio

#pylint: disable=redefined-outer-name

@pytest.fixture
def api_key():
    """ Returns a fake API key. """
    return 'PYTHON_API_CLIENT_TEST_KEY'

@pytest.fixture
def api_options():
    """ Returns an example dictionary configuration. """
    return {'debug': True}

@pytest.fixture
def api(api_key, api_options):
    """ Returns an instance of the API. """
    return skylab_studio.api(api_key, **api_options)

def test_api_no_key():
    """ Test api host setting. """
    with pytest.raises(Exception):
        skylab_studio.api(None)

def test_api_host():
    """ Test api host setting. """
    assert skylab_studio.api('KEY', api_host='test.com').api_host == 'test.com'

def test_api_proto():
    """ Test api proto setting. """
    assert skylab_studio.api('KEY', api_proto='http').api_proto == 'http'

def test_api_port():
    """ Test api port setting. """
    assert skylab_studio.api('KEY', api_port='80').api_port == '80'

def test_api_version():
    """ Test api version setting. """
    assert skylab_studio.api('KEY', api_version='2').api_version == '2'

def test_api_debug():
    """ Test api debug setting. """
    assert skylab_studio.api('KEY', debug=True).debug is True

def test_list_jobs(api):
    """ Test list jobs endpoint. """
    with requests_mock.Mocker() as mock:
        mock.get('https://studio.skylabtech.ai:443/api/v1/jobs', text='data')
        result = api.list_jobs()
        assert result.status_code == 200

def test_create_job(api):
    """ Test list jobs endpoint. """
    with requests_mock.Mocker() as mock:
        mock.post('https://studio.skylabtech.ai:443/api/v1/jobs', text='data')
        payload = {
            'foo': 'bar'
        }
        result = api.create_job(payload=payload)
        assert result.status_code == 200

def test_get_job(api):
    """ Test list jobs endpoint. """
    with requests_mock.Mocker() as mock:
        mock.get('https://studio.skylabtech.ai:443/api/v1/jobs/1', text='data')
        result = api.get_job(job_id=1)
        assert result.status_code == 200

def test_update_job(api):
    """ Test list jobs endpoint. """
    with requests_mock.Mocker() as mock:
        mock.put('https://studio.skylabtech.ai:443/api/v1/jobs/1', text='data')
        payload = {
            'foo': 'bar'
        }
        result = api.update_job(job_id=1, payload=payload)
        assert result.status_code == 200

def test_delete_job(api):
    """ Test list jobs endpoint. """
    with requests_mock.Mocker() as mock:
        mock.delete('https://studio.skylabtech.ai:443/api/v1/jobs/1', text='data')
        result = api.delete_job(job_id=1)
        assert result.status_code == 200

def test_process_job(api):
    """ Test list jobs endpoint. """
    with requests_mock.Mocker() as mock:
        mock.post('https://studio.skylabtech.ai:443/api/v1/jobs/1/process', text='data')
        result = api.process_job(job_id=1)
        assert result.status_code == 200

def test_cancel_job(api):
    """ Test list jobs endpoint. """
    with requests_mock.Mocker() as mock:
        mock.post('https://studio.skylabtech.ai:443/api/v1/jobs/1/cancel', text='data')
        result = api.cancel_job(job_id=1)
        assert result.status_code == 200

def test_list_profiles(api):
    """ Test list profiles endpoint. """
    with requests_mock.Mocker() as mock:
        mock.get('https://studio.skylabtech.ai:443/api/v1/profiles', text='data')
        result = api.list_profiles()
        assert result.status_code == 200

def test_create_profile(api):
    """ Test list profiles endpoint. """
    with requests_mock.Mocker() as mock:
        mock.post('https://studio.skylabtech.ai:443/api/v1/profiles', text='data')
        payload = {
            'foo': 'bar'
        }
        result = api.create_profile(payload=payload)
        assert result.status_code == 200

def test_get_profile(api):
    """ Test list profiles endpoint. """
    with requests_mock.Mocker() as mock:
        mock.get('https://studio.skylabtech.ai:443/api/v1/profiles/1', text='data')
        result = api.get_profile(profile_id=1)
        assert result.status_code == 200

def test_update_profile(api):
    """ Test list profiles endpoint. """
    with requests_mock.Mocker() as mock:
        mock.put('https://studio.skylabtech.ai:443/api/v1/profiles/1', text='data')
        payload = {
            'foo': 'bar'
        }
        result = api.update_profile(profile_id=1, payload=payload)
        assert result.status_code == 200

def test_delete_profile(api):
    """ Test list profiles endpoint. """
    with requests_mock.Mocker() as mock:
        mock.delete('https://studio.skylabtech.ai:443/api/v1/profiles/1', text='data')
        result = api.delete_profile(profile_id=1)
        assert result.status_code == 200

def test_list_photos(api):
    """ Test list photos endpoint. """
    with requests_mock.Mocker() as mock:
        mock.get('https://studio.skylabtech.ai:443/api/v1/photos', text='data')
        result = api.list_photos()
        assert result.status_code == 200

def test_create_photo(api):
    """ Test list photos endpoint. """
    with requests_mock.Mocker() as mock:
        mock.post('https://studio.skylabtech.ai:443/api/v1/photos', text='data')
        payload = {
            'foo': 'bar'
        }
        result = api.create_photo(payload=payload)
        assert result.status_code == 200

def test_get_photo(api):
    """ Test list photos endpoint. """
    with requests_mock.Mocker() as mock:
        mock.get('https://studio.skylabtech.ai:443/api/v1/photos/1', text='data')
        result = api.get_photo(photo_id=1)
        assert result.status_code == 200

def test_update_photo(api):
    """ Test list photos endpoint. """
    with requests_mock.Mocker() as mock:
        mock.put('https://studio.skylabtech.ai:443/api/v1/photos/1', text='data')
        payload = {
            'foo': 'bar'
        }
        result = api.update_photo(photo_id=1, payload=payload)
        assert result.status_code == 200

def test_delete_photo(api):
    """ Test list photos endpoint. """
    with requests_mock.Mocker() as mock:
        mock.delete('https://studio.skylabtech.ai:443/api/v1/photos/1', text='data')
        result = api.delete_photo(photo_id=1)
        assert result.status_code == 200
