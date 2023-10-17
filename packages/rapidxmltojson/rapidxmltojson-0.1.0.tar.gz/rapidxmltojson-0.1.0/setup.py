from setuptools import setup, Extension
from Cython.Build import cythonize


with open('README.md', 'r') as f:
    long_description = f.read()


extension = Extension(
    name='rapidxmltojson',
    sources=['rapidxmltojson.pyx'],
    include_dirs=['include'],
    language='c++',
)


setup(
    name='rapidxmltojson',
    description='rapidxmltojson',
    version='0.1.0',
    author='Alisher Nazarkhanov',
    author_email='alisher.nazarkhanov.dev@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nazarkhanov/rapidxmltojson',
    ext_modules=cythonize([extension]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Text Processing :: Markup :: XML',
    ],
)
