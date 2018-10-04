BioPrint
=========

BioPrint provides a  web interface for controlling a the BioBot1 3D Biomaterial printer

Packaging
------------

1. Install [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html) on your host OS
2. Install required Python modules in `bioprint` with `pip install -r requirements.txt`
3. Run `pyinstaller Bioprint.spec`
4. Executables are in `bioprint/dist`
5. For Windows: Download and install [Inno Setup](http://www.jrsoftware.org/isinfo.php) and use Bioprint.iss to package the executable into an installer

Installation
------------

### Windows

1. Install [Python 2.7](https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi).
2. Download [Bioprint 1.0](https://github.com/biobotsdev/bioprint/archive/1.0.zip) and extract to desired location on your computer.
3. Navigate to `bioprint-1.0/Windows` folder on your file system.
4. Right-click `Install.bat` file and "Run As Administrator".
5. Double-click `Bioprint.bat` and leave the Command Prompt Window open.
6. Navigate to [bioprint](http://bioprint/) in your browser.
7. Setup a username and password to use with Bioprint.
8. Begin printing with life!

### Mac OSX

1. Install [Python 2.7](https://www.python.org/ftp/python/2.7.11/python-2.7.11-macosx10.6.pkg).
2. Download [Bioprint 1.0](https://github.com/biobotsdev/bioprint/archive/1.0.zip) and extract to desired location on your computer.
3. Navigate to `bioprint-1.0/MacOSX` folder on your file system.
4. Double-click `Install.command` and enter your Administrator password when prompted
5. Double-click `Bioprint.command` and leave the Terminal Window open.
6. Navigate to [bioprint](http://bioprint/) in your browser.
7. Setup a username and password to use with Bioprint.
8. Begin printing with life!
