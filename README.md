[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## The Prometheus Analysis Framework



## The Gaugi core:


## The Simulator:


## Build Status
| Branch | Build status |
|--------|--------------|
| master | [![pipeline status](https://gitlab.cern.ch/jodafons/prometheus/badges/master/pipeline.svg)](https://gitlab.cern.ch/jodafons/prometheus/commits/master) |


## Requirements

- root (https://gitlab.cern.ch/jodafons/root.git)
- boost
- numpy
- python (2.7)
- cmake 3


## Install the custom Root CERN package (Required)

The ROOT system provides a set of OO frameworks with all the functionality
needed to handle and analyze large amounts of data in a very efficient way.
Having the data defined as a set of objects, specialized storage methods are
used to get direct access to the separate attributes of the selected objects,
without having to touch the bulk of the data. Included are histograming
methods in an arbitrary number of dimensions, curve fitting, function
evaluation, minimization, graphics and visualization classes to allow
the easy setup of an analysis system that can query and process the data
interactively or in batch mode, as well as a general parallel processing
framework, PROOF, that can considerably speed up an analysis.


```bash
# in your root dir
mkdir .bin
cd .bin
# download the root
git clone https://gitlab.cern.ch/jodafons/root.git
# checkout the custom branch
git checkout v6-16-00-custom
# create the build dir
mkdir build
cd build
# apply the cmake 
cmake ..
# and compile
make -j4
```

Then use this commands to include the root into your path.

```bash
echo 'source ~/.bin/root/build/bin/thisroot.sh' >> ~/.bashrc
source $HOME/root/bin/thisroot.sh
```

Then use apt-get (or yum) to install other dependencies (steps marked with recommended are not obligatory):

```bash
# Install gcc and other developer tools
sudo apt-get install coreutils
# Install python
sudo apt-get install python
# Install needed CVS
sudo apt-get install git subversion
# (Recommended) Install numpy and scipy
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
# (Recommended) Install boost
sudo apt-get install libboost-all-dev
```

## Prepare the prometheus workspace

```bash
# dowload all submodules
source setup_module.sh
# put everything to master
source setup_module.sh --head
```



## Standalone Installation (Recommended)

```bash
# setup all standalone envs
source setup_standalone.sh
# build and compile
source buildthis.sh
# setup the libs and modules
source setup_prometheus
```

## Athena Installation

```bash
# setup all ATLAS envs
source setup_athena.sh
# build and compile
source buildthis.sh
# setup the libs and modules
source build/x86-*/setup.sh
```


## Contribution

- Dr. João Victor da Fonseca Pinto, UFRJ/COPPE, CERN/ATLAS (jodafons@cern.ch) [maintainer, developer]
- Dr. Werner Freund, UFRJ/COPPE, CERN/ATLAS (wsfreund@cern.ch) [developer]
- Msc. Micael Verissimo, UFRJ/COPPE, CERN/ATLAS (mverissi@cern.ch) [developer]


