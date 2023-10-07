# GeoRDPy
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![PyPI](https://img.shields.io/pypi/v/geordpy)](https://pypi.org/project/geordpy/)
[![Documentation](https://github.com/avitase/geordpy/actions/workflows/build_docs.yml/badge.svg)](https://avitase.github.io/geordpy/)
[![Test coverage](https://codecov.io/gh/avitase/geordpy/graph/badge.svg?token=NHC60PVVEV)](https://codecov.io/gh/avitase/geordpy)
[![Unit tests](https://github.com/avitase/geordpy/actions/workflows/run_tests.yml/badge.svg)](https://codecov.io/gh/avitase/geordpy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

GeoRDPy is a Python library that simplifies geodetic-coordinate polylines using the Ramer-Douglas-Peucker algorithm. By default, it utilizes the distance to great-circle segments as the distance metric to reduce the number of points in a polyline while maintaining accuracy.
Optionally, the segments can be interpolated with rhumb lines instead of great-circle. For both options, the great-circle distance is used internally for finding the smallest distance between the interpolated segment and geodetic-coordinate points.

## Installation
GeoRDPy releases are available as wheel packages for macOS, Windows and Linux on [PyPI](https://pypi.org/project/geordpy/).
Install it using pip:
```bash
$ pip install geordpy
```

## Example Usage
The GeoRDPy API is designed with simplicity in mind, featuring a single method called `geordpy.rdp_filter`:
```python
>>> import geordpy
>>> points = [(latitude1, longitude1), (latitude2, longitude2), ...]
>>> threshold = 15_000  # meters
>>> mask = geordpy.rdp_filter(points, threshold)
>>> trajectory = np.array(points)[mask]
```
For a quick illustration of how to utilize this method, refer to the [example here](https://github.com/avitase/geordpy/blob/main/geordpy/example.py).

For more details, check the [documentation](https://avitase.github.io/geordpy/).

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to submit a pull request.

### Development Setup
To set up your development environment, follow these steps:

1. Clone the repository:
   ```bash
   $ git clone https://github.com/avitase/geordpy.git
   ```

2. Change to the project directory:
   ```bash
   $ cd geordpy
   ```

3. Install the development dependencies using `pip`:
   ```bash
   $ pip install -e .[dev]
   ```

### Pre-Commit-Hooks
To maintain code quality and avoid pushing invalid commits, we recommend using pre-commit hooks. These hooks perform automated checks before commits are made. To set up pre-commit hooks, follow these steps:

1. Install the pre-commit package (if not already installed):
   ```bash
   $ pip install pre-commit
   ```

2. Install the hooks:
   ```bash
   $ pre-commit install
   ```

Now, each time you commit changes, the pre-commit hooks will run checks such as formatting, linting, and more. If any issues are found, they will be flagged before the commit is made.

### Running Tests
You can run tests using the following command:
```bash
$ pytest
```

Make sure to run tests before submitting a pull request to ensure that everything is functioning as expected.
