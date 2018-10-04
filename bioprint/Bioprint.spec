# -*- mode: python -*-

block_cipher = None


a = Analysis(['Bioprint.py'],
             pathex=['/Users/nick/Desktop/bioprint-devel/bioprint', '/Users/nick/Desktop/bioprint-devel/bioprint/src'],
             binaries=[],
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
          console=False , icon='allevi.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Allevi Bioprint')
app = BUNDLE(coll,
             name='Allevi Bioprint.app',
             icon='allevi.icns',
             bundle_identifier=None,
             info_plist={
                'LSUIElement': True,
                }
            )
