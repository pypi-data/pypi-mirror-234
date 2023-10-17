from setuptools import setup, Extension
from Cython.Build import cythonize


extension = Extension(
    name='rapidxmltojson',
    sources=['rapidxmltojson.pyx'],
    package_data=['rapidxmltojson.pyi'],
    include_dirs=['include'],
    language='c++',
)


setup(
    name='rapidxmltojson',
    ext_modules=cythonize([extension]),
)
