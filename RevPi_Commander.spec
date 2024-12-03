# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\revpicommander\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('dist/bundled-libraries.md', 'revpicommander\\open-source-licenses'), ('dist/open-source-licenses.*', 'revpicommander\\open-source-licenses'), ('src\\revpicommander\\locale', '.\\revpicommander\\locale'), ('data\\revpicommander.ico', '.')],
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
    name='RevPi Commander',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['data\\revpicommander.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RevPi Commander',
)
