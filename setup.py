try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='grading',
      version='0.0.1',
      description='Authoring and grading of notebook assignments',
      long_description='Authoring and grading of notebook assignments',
      license='BSD',
      author='UC Boulder Earthlab',
      packages=['grading'],
      install_requires=['nbclean', 'jinja2'],
      include_package_data=True,
      entry_points={
        'console_scripts': [
            'nbgrade = grading.__main__:grade',
            'nbauthor = grading.__main__:author',
            'nbdistribute = grading.__main__:distribute',
        ]
},
)
