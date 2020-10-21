#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

  # install conda and the abc-dev environment
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
  bash ~/miniconda.sh -b -p $HOME/miniconda
  export PATH="$HOME/miniconda/bin:$PATH"
  echo "conda activate base" >> ~/.bashrc
  source $HOME/miniconda/bin/activate
  conda config --set always_yes yes --set show_channel_urls true --set changeps1 no
  conda update -q conda
  conda config --add channels conda-forge
  conda info -a
  conda init bash
  conda env create -f environment.yml
  conda activate abc-dev
  python setup.py install
  conda info -a
  pip install -r dev-requirements.txt
  conda info -a

else
  sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable --yes
  sudo apt-get update
  pip install tox-travis
fi
