# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\vnich\\YandexDisk\\ProductParsing\\scripts'],
             binaries=[],
             datas=[('database/LeroyMerlin/ad_leroy_merlin.py', '.'),
                    ('database/__all_models.py', '.'),
                    ('database/db_session.py', '.'),
                    ('LeroyMerlin/ParsingAd.py', '.'),
                    ('LeroyMerlin/ParsingPage.py', '.'),
                    ('Errors.py', '.'),
                    ('GettingDriver.py', '.'),
                    ('interface.py', '.'),],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
