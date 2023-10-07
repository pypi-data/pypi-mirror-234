import pathlib
import re

import setuptools

# parse version number
version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
version_file_contents = pathlib.Path('fiddler', '_version.py').open().read()
version_match = re.search(version_regex, version_file_contents, re.M)
if version_match:
    version = version_match.group(1)
else:
    raise RuntimeError('Unable to find version string.')


with open('PUBLIC.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fiddler-client',
    version=version,
    author='Fiddler Labs',
    description='Python client for Fiddler Service',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://fiddler.ai',
    packages=setuptools.find_packages(),
    install_requires=[
        'pip>=21.0',
        'requests<3',
        'requests-toolbelt',
        'pandas>=1.2.5,<=1.5.3',
        'pydantic==1.9.0',
        'deprecated==1.2.13',
        'tqdm==4.64.1',
        'simplejson>=3.17.0',
        'pyarrow>=12.0.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>3.6.3',
)
