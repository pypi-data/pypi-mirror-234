# -*- mode: python ; coding: utf-8 -*-

added_files = [
	('pyrateshield/constants.yml', 'pyrateshield'),
	('pyrateshield/defaults.yml', 'pyrateshield'),
	('pyrateshield/LICENSE', 'pyrateshield'),
	('icon.ico', 'pyrateshield'),
	
	('pyrateshield/isotopes.yml', 'pyrateshield'),
	
	('pyrateshield/gui/toolbar.yml', 'pyrateshield/gui'),
	('pyrateshield/gui/icon.png', 'pyrateshield/gui'),
	('pyrateshield/gui/splash.png', 'pyrateshield/gui'),
	('pyrateshield/radtracer/MCNP.pickle', 'pyrateshield/radtracer'),
	
	('pyrateshield/pyshield/attenuation.xls', 'pyrateshield/pyshield'),
	('pyrateshield/pyshield/buildup.xls', 'pyrateshield/pyshield')
	
]

block_cipher = None

a = Analysis(['pyrateshield/app.py'],
             pathex=['.'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
             
splash = Splash(
    'pyrateshield/gui/splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          splash,
          splash.binaries,

          name='pyrateshield_app', #MS: cannot use pyrateshield, build fails on macos. On window it builds to pyratehsield.exe on mac to pyrateshield which is also a folder
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
		  icon='./icon.ico')
'''
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pyrateshield')
'''