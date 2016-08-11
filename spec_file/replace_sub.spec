# -*- mode: python -*-

block_cipher = None


a = Analysis(['d:\\github\\AJ-sub\\main.py'],
             pathex=['c:\\', 'C:\\Python35\\Scripts'],
             binaries=None,
             datas=
			 [('D:\\github\\AJ-sub\\Settings.ini','.'),
			 ('D:\\github\\AJ-sub\\SubList.sdb','.'),
			 ('D:\\github\\AJ-sub\\txt_map\\opencc\\config\\*','opencc\\config'),
			 ('D:\\github\\AJ-sub\\txt_map\\opencc\\dictionary\\*','opencc\\dictionary')
			 ],
			 
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
          exclude_binaries=True,
          name='replace_sub',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='replace_sub')
