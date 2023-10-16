# viso-sdk-python

**viso-sdk-python** is a utility for [viso.ai](https://viso.ai) containers.

## Installation

Use `pip` to install the latest stable version of **viso-sdk-python**:

```shell
pip install viso-sdk-python
```


## Build
```shell
python3 -m pip install -e .
python3 setup.py sdist bdist_wheel

# pip3 install setuptools-cythonize
# pip3 install setuptools
# pip3 install --upgrade pip
```

```shell
- remove build files before pushing
cd viso_sdk
find . -type f -name "*.c" -delete
find . -type f -name "*.so" -delete
```