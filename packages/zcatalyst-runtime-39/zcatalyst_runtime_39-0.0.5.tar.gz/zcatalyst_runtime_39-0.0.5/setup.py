import os
import json
import shutil

from setuptools import setup
from distutils.cmd import Command

# cwd example: /tmp/zcatalyst_runtime_3x-0.1.0
PY_PACKAGE_NAME = os.getcwd().split('/').pop().split('-')[0]

meta = {}
with open(f'{PY_PACKAGE_NAME}/meta.json') as meta_file:
    meta = json.load(meta_file)

class CleanCommand(Command):
    """Custom cleanup procedure"""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree('dist/')
        shutil.rmtree(f'{PY_PACKAGE_NAME}.egg-info')

setup(
    name=meta['name'],
    version=meta['version'],
    description=f"{meta['description']}-{os.getenv('COMMIT_HASH')}",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author=meta['maintainer'],
    author_email=meta['maintainer_email'],
    maintainer=meta['maintainer'],
    maintainer_email=meta['maintainer_email'],
    keywords=meta['keywords'],
    license='Apache 2.0',
    url='https://catalyst.zoho.com/',
    include_package_data=True, 
    cmdclass={
        'clean': CleanCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
    ],
)