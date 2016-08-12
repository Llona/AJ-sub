# -*- mode: python -*-

block_cipher = None


a = Analysis(['D:\\github\\AJ-sub\\main.py'],
             pathex=['C:\\Python35\\Scripts'],
              binaries=None,
             datas=
			 [('D:\\github\\AJ-sub\\Settings.ini','.'),
			 ('D:\\github\\AJ-sub\\SubList.sdb','.'),
			 ('D:\\github\\AJ-sub\\txt_map\\opencc\\config\\*','opencc\\config'),
			 ('D:\\github\\AJ-sub\\txt_map\\opencc\\dictionary\\*','opencc\\dictionary'),
			 ('D:\\github\\AJ-sub\\icons\\*','icons'),
			 ('D:\\github\\AJ-sub\\NOTICE.txt','.'),
			 ('D:\\github\\AJ-sub\\LICENSE','.')
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
          name='AJSub',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='D:\\github\\AJ-sub\\AJSub.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='AJSub')
