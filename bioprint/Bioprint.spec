# -*- mode: python -*-
import sys, os

BIOPRINT_VERSION = '1.5.0'

#  Platform-specific icons and binaries
icon = 'allevi.icns'
msvcp_binaries = []
if sys.platform == 'win32':
    # Include MSCVP libs on Windows
    msvcp_binaries = [('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'),
                ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY')]
    #  Windows uses .cio instead of .icns
    icon = 'allevi.ico'

block_cipher = None

a = Analysis(['Bioprint.py'],
             pathex=['.', 'src'],
             binaries=[
                ('/System/Library/Frameworks/Tk.framework/Tk', 'tk'),
                ('/System/Library/Frameworks/Tcl.framework/Tcl', 'tcl')
             ],
             datas=[
                ('allevi.png', '.'),
                ('allevi.png', 'bioprint/static'),
                ('allevi-114.png', 'bioprint/static'),
                ('allevi-144.png', 'bioprint/static'),
                ('allevi.ico', 'bioprint/static'),
                ('src/bioprint/static', 'bioprint/static'),
                ('src/bioprint/templates', 'bioprint/templates'),
                ('src/bioprint/plugins', 'bioprint/plugins'),
                ('src/bioprint/translations', 'bioprint/translations'),
                ],
             hiddenimports=['bioprint', '_sysconfigdata', 'HTMLParser'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Allevi Bioprint',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon=icon)

coll = COLLECT(exe,
               a.binaries + msvcp_binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Allevi Bioprint')

#  Bundle .app on OS X
if sys.platform == 'darwin':
    app = BUNDLE(coll,
                 name='Allevi Bioprint.app',
                 icon='allevi.icns',
                 bundle_identifier=None,
                 info_plist={
                    'NSPrincipalClass': 'NSApplication',
                    'CFBundleName': 'Bioprint',
                    'CFBundleDisplayName': 'Allevi Bioprint',
                    'CFBundleIdentifier': 'org.allevi.bioprint',
                    'CFBundleVersion': BIOPRINT_VERSION,
                    'CFBundleShortVersionString': BIOPRINT_VERSION,
                    'LSUIElement': True,
                    }
                )