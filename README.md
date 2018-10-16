BioPrint
=========

BioPrint provides a  web interface for controlling a the BioBot1 3D Biomaterial printer


Packaging
------------

1. Install [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html) on your host OS
2. Install required Python modules in `bioprint` with `pip install -r requirements.txt`
2a. For OSX you'll need an older version to build a compatible executable. Try 10.8.
2b. For Windows you'll need the [VC 2008](http://download.microsoft.com/download/d/2/4/d242c3fb-da5a-4542-ad66-f9661d0a8d19/vcredist_x64.exe) and [VC 2010](http://download.microsoft.com/download/3/2/2/3224B87F-CFA0-4E70-BDA3-3DE650EFEBA5/vcredist_x64.exe) redistributables, as well as the [VC++ compiler for Python 2.7]( http://aka.ms/vcpython27)
3. Run `pyinstaller Bioprint.spec`
4a. Executables are in `bioprint/dist` for OSX. Sign the .app, and add it to a .dmg bundle using [DMG Canvas](https://www.araelium.com/dmgcanvas) using the `Bioprint.dmgCanvas` template.
4b. For Windows: Download and install [Inno Setup](http://www.jrsoftware.org/isinfo.php) and open Bioprint.iss, then click `Compile` to package the executable into an installer. You'll find the installer package in `bioprint/Output`. *Code signing is enabled as part of the Inno Setup config, which will fail without the proper dependencies and certificates. See below for additional requirements.*


Signing
------------

### Windows

1. Install the [Windows SDK](http://go.microsoft.com/fwlink/p/?linkid=84091). You only need the Tools, not Samples, Windows Headers, etc.
2. Ensure that a valid code signing certificate exists in `bioprint`. Ours is provided by Comodo CA.
3. In Inno Setup, go to Tools -> Configure Sign Tools... and add a new sign tool named MSSignTool with the command `"C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\signtool.exe" sign /f Allevi_Comodo_Code_Signing_Cert.p12 /p [PASSWORD] /tr "http://timestamp.comodoca.com" /td sha256 /fd sha256 /a $p`. Replace `[PASSWORD]` with our CV certificate password.
4. Compile the installer with Inno Setup, and signing should occur automatically. See `bioprint/Output` for the final exe.

### Mac OSX

1. Ensure that an Apple Developer ID Application code signing certificate is installed. Xcode -> Preferences -> Accounts -> Manage Certificates
2. Run `codesign --force --deep --verify --verbose --sign "Developer ID Application: Allevi Inc." "Allevi Bioprint.app"`
