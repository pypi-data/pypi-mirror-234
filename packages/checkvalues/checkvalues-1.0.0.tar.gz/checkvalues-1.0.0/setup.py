import re
import sys

import setuptools
import os


if sys.version_info < (3, 7):
    sys.exit('Python < 3.7 is not supported')


# get abs path from this folder name
here = os.path.dirname(os.path.abspath(__file__))
print(here)

# open __init__.py, where version is specified
with open(os.path.join(here, 'checkvalues', '__init__.py')) as f:
    txt = f.read()


# try to read it from source code
try:
    version = re.findall(r"^__version__ = '([^']+)'\r?$",
                         txt, re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')

# get long description from file in docs folder
#with open(os.path.join(here, 'docs/project_description.md')) as f:
#    long_description = f.read()


# function to read requirements, and include them as package dependencies
def get_requirements(*files):
    # read requirements.txt file and return them as a list of strings
    reqs = []
    for file in files:
        with open(file) as f:
            req = f.readlines()
        reqs += [r.strip() for r in req]
    return reqs  # clean lines from blank spaces and line breaks

setuptools.setup(
    name="checkvalues", # Replace with your own username
    version=version,
    author="Rafael Cabañas",
    author_email="rcabanas@ual.es",
    description="checkvalues",
#    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PGM-Lab/bcause",

    packages=["checkvalues"],
    include_package_data=True,
    license='Apache License 2.0',
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Programming Language :: Python :: 3.8'],
    python_requires='>=3.8',
    # install_requires=get_requirements('requirements.txt'),
    install_requires=["pandas >1.1, <2.1",
"numpy>1.22, <1.26"]
    #extras_require=dict(tests=['pytest'])
)