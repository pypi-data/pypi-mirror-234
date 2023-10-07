# Skylab Studio Python Client

[![CircleCI](https://circleci.com/gh/skylab-tech/studio_client_python.svg?style=svg)](https://circleci.com/gh/skylab-tech/studio_client_python)
[![Maintainability](https://api.codeclimate.com/v1/badges/6e3316f60d72a9ca9276/maintainability)](https://codeclimate.com/github/skylab-tech/studio_client_python/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6e3316f60d72a9ca9276/test_coverage)](https://codeclimate.com/github/skylab-tech/studio_client_python/test_coverage)

SkylabTech Studio Python client.

[studio.skylabtech.ai](https://studio.skylabtech.ai)

## Requirements

- [Python requests library](http://docs.python-requests.org/en/master/user/install/#install)

## Installation

```bash
$ pip install skylab_studio
```

## Usage

For all examples, assume:

```python
import skylab_studio

api = skylab_studio.api(api_key='YOUR-API-KEY')
```

### Error Handling

By default, the API calls return a response object no matter the type of response.

### Endpoints

#### List all jobs

```python
api.list_jobs()
```

#### Create job

```python
payload = {
  'profile_id': 1
}

api.create_job(payload=payload)
```

For all payload options, consult the [API documentation](http://docs.studio.skylabtech.ai/#operation/createJob).

#### Get job

```python
api.get_job(job_id)
```

#### Update job

```python
payload = {
  'profile_id': 2
}

api.create_job(job_id, payload=payload)
```

For all payload options, consult the [API documentation](http://docs.studio.skylabtech.ai/#operation/updateJobById).

#### Delete job

```python
api.delete_job(job_id)
```

#### Process job

```python
api.process_job(job_id)
```

#### Cancel job

```python
api.cancel_job(job_id)
```

#### List all profiles

```python
api.list_profiles()
```

#### Create profile

```python
payload = {
  'name': 'My profile'
}

api.create_profile(payload=payload)
```

For all payload options, consult the [API documentation](http://docs.studio.skylabtech.ai/#operation/createProfile).

#### Get profile

```python
api.get_profile(profile_id)
```

#### Update profile

```python
payload = {
  'name': 'My profile'
}

api.create_profile(profile_id, payload=payload)
```

For all payload options, consult the [API documentation](http://docs.studio.skylabtech.ai/#operation/updateProfileById).

#### List all photos

```python
api.list_photos()
```

#### Create photo

```python
payload = {
  'image': 'some-base64-string'
}

api.create_photo(payload=payload)
```

For all payload options, consult the [API documentation](http://docs.studio.skylabtech.ai/#operation/createPhoto).

#### Get photo

```python
api.get_photo(photo_id)
```

#### Upload photo

##### upload_photo(photo_path, model, model_id, skip_cache=False)

model can either be 'job' or 'profile'

model_id is the jobs/profiles respective id

```python
api.upload_photo('/path/to/photo', 'job', job_id)
```

#### Update photo

```python
payload = {
  'image': 'some-base64-string'
}

api.create_photo(photo_id, payload=payload)
```

For all payload options, consult the [API documentation](http://docs.studio.skylabtech.ai/#operation/updatePhotoById).

#### Delete photo

```python
api.delete_photo(photo_id)
```

### Expected Responses

#### Success

```bash
    >>> response.status_code
    200

    >>> response.json().get('success')
    True

    >>> response.json().get('status')
    u'OK'

    >>> response.json().get('profile_id')
    u'numeric-profile-id'
```

#### Error

- Malformed request

```bash
    >>> response.status_code
    422
```

- Bad API key

```bash
    >>> response.status_code
    403
```

## Testing

To run the test suite:

```bash
pytest
```

To run the test suite with code coverage metrics:

```bash
pytest --cov-report --cov=skylab_studio
```

## Troubleshooting

### General Troubleshooting

- Enable debug mode
- Make sure you're using the latest Python client
- Capture the response data and check your logs &mdash; often this will have the exact error

### Enable Debug Mode

Debug mode prints out the underlying request information as well as the data
payload that gets sent to Studio. You will most likely find this information
in your logs. To enable it, simply put `debug=True` as a parameter when instantiating
the API object. Use the debug mode to compare the data payload getting
sent to [Studio' API docs](http://docs.studio.skylabtech.ai/#).

```python
import skylab_studio

api = skylab_studio.api(api_key='YOUR-API-KEY', debug=True)
```

### Response Ranges

Studio' API typically sends responses back in these ranges:

- 2xx – Successful Request
- 4xx – Failed Request (Client error)
- 5xx – Failed Request (Server error)

If you're receiving an error in the 400 response range follow these steps:

- Double check the data and ID's getting passed to Studio
- Ensure your API key is correct
- Log and check the body of the response

## Distribution

To package:

```bash
  python setup.py sdist bdist_wheel
  python -m twine upload dist/*
```
