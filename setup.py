import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

DISTNAME = "abc-classroom"
DESCRIPTION = (
    "Efficiently manage github classroom assignments from the command line."
)
MAINTAINER = "Leah Wasser"
MAINTAINER_EMAIL = "leah.wasser@colorado.edu"

setup(
    name=DISTNAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version="0.1.8",
    license="BSD",
    packages=["abcclassroom"],
    install_requires=[
        "nbclean",
        "jinja2",
        "papermill",
        "nbformat",
        "ruamel.yaml",
        "github3.py",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    include_package_data=True,
    package_data={
        "abcclassroom": [
            "example-data/readme.md",
            "example-data/sample_roster.csv",
            "example-data/config.yml",
            "example-data/extra_files/README.md",
            "example-data/extra_files/.gitignore",
        ]
    },
    entry_points={
        "console_scripts": [
            "abc-init = abcclassroom.__main__:init",
            "abc-quickstart = abcclassroom.__main__:quickstart",
            "abc-new-template = abcclassroom.__main__:new_template",
            "abc-update-template = abcclassroom.__main__:update_template",
            "abc-clone = abcclassroom.__main__:clone",
            "abc-feedback = abcclassroom.__main__:feedback",
        ]
    },
    url="https://github.com/earthlab/abc-classroom",
)
