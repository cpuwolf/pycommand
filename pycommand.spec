# -*- mode: python -*-

block_cipher = None


a = Analysis(['pycommand.py'],
             pathex=['/Users/apple/code/pyff777wingflexfix'],
             binaries=[],
             datas=[('main.ui','.'),
             ('pycommand.cfg','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pycommand',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='logo.ico')
app = BUNDLE(exe,
             a.datas, 
             name='pycommand.app',
             icon='logo.icns')
