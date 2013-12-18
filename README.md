imgs-scripts
============

Various scripts to get images metrics

##Installation
Install virtualenv:

``` sh
$ sudo easy_install virtualenv
```

Download git repository:

``` sh
$ git clone https://github.com/uf0/imgs-scripts.git
```

browse to imgs-scripts root folder:

``` sh
$ cd imgs-scripts
```

You may need to install ```libjpeg```

``` sh
$ brew install libjpeg
```

Create a virtualenv directory `env`, activate the virtualenv and install the requirements:

``` sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
$ pip install -r requirements.txt
```
##Run scripts

###dominatio.py
This script gets in input a folder containing images and outputs a .tsv file with the HEX code of the dominant color(s).

Type `$ python dominatio.py -h` for usage instructions