try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='abc-classroom',
      version='0.0.1',
      description='Authoring and grading of notebook assignments',
      long_description='Authoring and grading of notebook assignments',
      license='BSD',
      author='UC Boulder Earthlab',
      packages=['abcclassrom'],
      install_requires=['nbclean',
                        'jinja2',
                        'papermill',
                        'nbformat',
                        'ruamel.yaml',
                        'github3.py'],
      include_package_data=True,
      entry_points={
        'console_scripts': [
            'abc-init = abcclassrom.__main__:init',
            'abc-grade = abcclassrom.__main__:grade',
            'abc-author = abcclassrom.__main__:author',
            'abc-distribute = abcclassrom.__main__:distribute',
        ]
        },
      )
