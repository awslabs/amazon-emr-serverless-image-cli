# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['..\\..\\amazon_emr_serverless_image_cli\\__main__.py'],
             pathex=['<absolute path to root>'],
             binaries=[],
             datas=[('..\\..\\amazon_emr_serverless_image_cli\\assets\\image-manifest.yaml', 'assets')],
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
          name='amazon-emr-serverless-image',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
