# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['whack_a_mole.py'],
    pathex=[],
    binaries=[],
    datas=[('sounds/*', 'sounds')],
    hiddenimports=['pyttsx3.drivers', 'pyttsx3.drivers.sapi5', 'pkg_resources.py2_warn', 'pygame._sdl2.audio'],
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
    a.binaries,
    a.datas,
    [],
    name='WhackAMole',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app.ico'],
)
