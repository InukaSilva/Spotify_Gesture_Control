# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

block_cipher = None  # Define block_cipher variable

a = Analysis(
    ['main.py'],  # Your main script
    pathex=['.'],
    binaries=[],
    datas=[
        ('Gesture_Control.task', '.'), 
        ('Tutorial.png', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SpotifyGestureController',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    version='1.0.0',
    specpath='.',
    cipher=block_cipher,
)

app = BUNDLE(
    exe,
    name='SpotifyGestureController.app',
    icon=None,
    bundle_identifier=None,
    info_plist={
        'CFBundleName': 'SpotifyGestureController',
        'CFBundleIdentifier': 'com.example.spotifygesturecontroller',
        'CFBundleVersion': '1.0.0',
        'CFBundleExecutable': 'SpotifyGestureController',
    },
    contains=[
        (a.pure, a.zipped_data)
    ],
    code_signing_identity=None
)