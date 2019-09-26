try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="abc-classroom",
    version="0.0.7",
    description="Efficiently manage github classroom assignments from the command line.",
    long_description="Authoring and grading of notebook assignments",
    license="BSD",
    author="Earth Lab, University of Colorado -- Boulder",
    packages=["abcclassroom"],
    install_requires=[
        "nbclean",
        "jinja2",
        "papermill",
        "nbformat",
        "ruamel.yaml",
        "github3.py",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "abc-init = abcclassroom.__main__:init",
            "abc-grade = abcclassroom.__main__:grade",
            "abc-author = abcclassroom.__main__:author",
            "abc-distribute = abcclassroom.__main__:distribute",
        ]
    },
)
