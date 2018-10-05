BioPrint
=========

BioPrint provides a  web interface for controlling a the BioBot1 3D Biomaterial printer


Packaging
------------

1. Install [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html) on your host OS
2. Install required Python modules in `bioprint` with `pip install -r requirements.txt`
2a. For Windows you'll need the [VC 2008](http://download.microsoft.com/download/d/2/4/d242c3fb-da5a-4542-ad66-f9661d0a8d19/vcredist_x64.exe) and [VC 2010](http://download.microsoft.com/download/3/2/2/3224B87F-CFA0-4E70-BDA3-3DE650EFEBA5/vcredist_x64.exe) redistributables, as well as the [VC++ compiler for Python 2.7]( http://aka.ms/vcpython27)
3. Run `pyinstaller Bioprint.spec`
4a. Executables are in `bioprint/dist` for OSX
4b. For Windows: Download and install [Inno Setup](http://www.jrsoftware.org/isinfo.php) and open Bioprint.iss, then click `Compile` to package the executable into an installer. You'll find the installer package in `bioprint/Output`


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
