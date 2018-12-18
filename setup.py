try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='abcnb',
      version='0.0.1',
      description='Authoring and grading of notebook assignments',
      long_description='Authoring and grading of notebook assignments',
      license='BSD',
      author='UC Boulder Earthlab',
      packages=['abcnb'],
      install_requires=['nbclean',
                        'jinja2',
                        'papermill',
                        'nbformat',
                        'ruamel.yaml',
                        'github3.py'],
      include_package_data=True,
      entry_points={
        'console_scripts': [
            'abc-init = abcnb.__main__:init',
            'abc-grade = abcnb.__main__:grade',
            'abc-author = abcnb.__main__:author',
            'abc-distribute = abcnb.__main__:distribute',
        ]
        },
      )
