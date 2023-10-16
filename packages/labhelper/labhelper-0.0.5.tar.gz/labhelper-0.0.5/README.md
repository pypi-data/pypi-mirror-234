# Lab-Helper

Basic python library to help with the boring parts of lab work (calculation the error function, making tables, finding the required value of a certain parameter in order to make the error function have a certain value, ...)
it is currently very much in development, some interesting things have been added, especially in the domain of symbolic computation, but it is quite bare-bones, I hope to add more to it not only this year but even during my Masters and/or PHD.

If anyone wants to contribute it would be very much appreciated, just submit a push request and I'll review and most likely accept it.

## Requirements
- Python 3.8+ (probably works on earlier versions but I haven't tested nor is there any point in doing so)
- Jupyter Notebooks (this library is specifically made for use in jupyter, it's not incompatible with regular python scripts, but it also probably won't work very well)

## Installation
If all you want is the working library you can either install it through `pip` as follows:
```
pip install labhelper
```
If you want to contribute you should clone the git repository, and install it locally instead of through pip:
```
cd C:\Whatever\Directory\You\Want //same as cd [Directory]
git clone https://github.com/Batres3/Lab-Helper.git
cd Lab-Helper
pip install .
```
## Contributing
Simply develop whichever new features you consider useful, the way to do this is to edit the files where you cloned the repository (I use Visual Studio Code), and whenever you want to test a change you have make simply do the following (inside the ./Lab-Helper directory):
```
pip uninstall labhelper
pip install .
```
Now when you put `import labhelper as hp` into a new python environment, it will load the changes you have made to it

## Usage
In order to use this package simply go into a new Jupyter Notebook and, just like any other python package, write `import labhelper as hp` at the very top
When you want to use a function from the library simply do:
```
hp.[name of whatever you want to use]
```
You can also do `from labhelper import *` instead of `import labhelper as hp` this will make it so you don't have to add `hp.` in front of every function, although I personally prefer adding it
## Issues
You can either post the issues in the `Issues` tab at the top of the github site, or contact me personally.
