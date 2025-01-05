# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Program.py'],
    pathex=['/Users/krishkushwaha/Projects/GitHub Repos/Shashthi-The-Hunter/Scripts'],
    binaries=[],
    datas=[
        ('/Users/krishkushwaha/Projects/GitHub Repos/Shashthi-The-Hunter/Sprites', 'Sprites')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ShashthiTheHunter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ShashthiTheHunter',
)