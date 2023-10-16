import os
import setuptools

__version__ = '1.5'

try:
    if os.environ['GIT_BRANCH'] == 'master':
        __version__ += '.dev' + os.environ['BUILD_NUMBER']
except KeyError:
    pass

setuptools.setup(version=__version__)
