# -*- mode: python -*-

block_cipher = None

added_files = [
    ('src/user_interface/home_screen_pic.png','src/user_interface'),
    ('src/user_interface/error_screen_pic.png','src/user_interface'),
    ('src/user_interface/wait_screen_pic.png','src/user_interface')
]

a = Analysis(
    ['src/rostering_app.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={
        "matplotlib": {
            "backends": "pdf",
        },
    },
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WLLRRosterApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    icon='rostering_app_icon.ico'
)
