from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize("src/imppkg/harmonic_mean.pyx"),
)
