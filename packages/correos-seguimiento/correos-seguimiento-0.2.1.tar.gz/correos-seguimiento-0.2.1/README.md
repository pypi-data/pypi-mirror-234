[![pipeline status](https://git.coopdevs.org/coopdevs/som-connexio/correos/correos-seguimiento/badges/main/pipeline.svg)](https://git.coopdevs.org/coopdevs/som-connexio/correos/correos-seguimiento/commits/master)
[![coverage report](https://git.coopdevs.org/coopdevs/som-connexio/correos/correos-seguimiento/badges/main/coverage.svg)](https://git.coopdevs.org/coopdevs/som-connexio/correos/correos-seguimiento/commits/master)

:warning: WORK IN PROGRESS :warning:

This library is a Python wrapper for accessing Seguimiento Correos JSON API.


## Operations

*  The API will provide all the necessary data for tracking a shipment. With this module you can check if the parcel is already delivered or relabeled and get the new tracking code.

More info about the API in [docs](docs/README.md).

## Installation

```commandline
$ pip install correos-seguimiento
```

## Usage

#### Check if shipment is delivered

```python
>>> from correos_seguimiento.services.shipment import TrackingShipment
>>>
>>> shipment = TrackingShipment("XXX", "XXX", "PQXXX10721392610108021C").build()
>>> shipment.is_delivered()
False
>>> shipment.is_delivered()
True
```

#### Check if shipment is relabeled and get the new tracking code

```python
>>> from correos_seguimiento.services.shipment import TrackingShipment
>>>
>>> shipment = TrackingShipment("XXX", "XXX", "PQXXX10721392610108021C").build()
>>> shipment.is_delivered()
False
>>> shipment.is_relabeled()
True
>>> shipment.get_relabeled_shipment_code()
"PY53VM9100000810108640T"
```

## Development

### Setup environment

1. Install `pyenv`
```sh
curl https://pyenv.run | bash
```
2. Build the Python version
```sh
pyenv install  3.7.13
```
3. Create a virtualenv
```sh
pyenv virtualenv 3.7.13 correos-seguimiento
```
4. Install dependencies
```sh
pyenv exec pip install -r requirements.txt
```
5. Install pre-commit hooks
```sh
pyenv exec pre-commit install
```

### Test the HTTP request

We are using the HTTP recording plugin of Pytest: [pytest-recording](https://pytest-vcr.readthedocs.io/).

With VRC we can catch the HTTP responses and then, execute the tests using them.

To add a new test:

* Expose the needed envvars. Look for them at the [Configuration Environment section](#configuration-environment)
* Execute the tests using `pytest` command:
* If you are writing a new test that is making requests, you should run:

```commandline
$ pytest --record-mode=once path/to/your/test
```

* You might need to record requests for an specific tests. In that case make sure to only run the tests affected and run

```commandline
$ pytest --record-mode=rewrite path/to/your/test
```

* Add the new `cassetes` to the commit and push them.
* The CI uses the cassetes to emulate the HTTP response in the test.

### Run test suite

```commandline
$ tox
```

### Formatting

We use [Black](https://github.com/psf/black) as formatter.
First to commit, tun the `black` command:

```commandline
$ black .
All done! ✨ 🍰 ✨
29 files left unchanged.
```

#### Darker

Black is a great formatter, but to mantain your code without execute the `black` command avery time, you can configure your IDE to use [darker](https://pypi.org/project/darker/) to format only the changed or added code when you save the file.

### Release process

Update CHANGELOG.md following this steps:

1. Add any entries missing from merged merge requests.
1. Duplicate the `[Unreleased]` header.
1. Replace the second `Unreleased` with a version number followed by the current date. Copy the exact format from previous releases.

Then, you can release and publish the package to PyPi:

1. Update the `__version__` var in `__init__.py` matching the version you specified in the CHANGELOG.
1. Open a merge request with these changes for the team to approve
1. Merge it, add a git tag on that merge commit and push it.
1. Once the pipeline has successfully passed, your package had been published.
