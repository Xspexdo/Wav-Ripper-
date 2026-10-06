# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# Ensure PATH does not contain Adoptium / Java / Windows Kits shadowing system DLLs
clean_path = ';'.join([p for p in os.environ.get('PATH', '').split(';') if 'adoptium' not in p.lower() and 'java' not in p.lower() and 'windows kits' not in p.lower()])
os.environ['PATH'] = clean_path

from PyInstaller.utils.hooks import collect_all

datas = [('logo_rounded.png', '.'), ('logo.ico', '.')]
binaries = []
hiddenimports = []
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['wav_hud.pyw'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'scipy', 'matplotlib', 'pandas', 'IPython', 'unittest', 'test'],
    noarchive=False,
    optimize=0,
)

# Strip out Windows API set forwarders and any JDK/Windows Kits binaries.
# Windows OS (10 & 11) natively provides ucrtbase.dll and all api-ms-win-* sets.
# Bundling them from third-party locations breaks LoadLibrary on target machines.
a.binaries = [
    b for b in a.binaries
    if not b[0].lower().startswith('api-ms-win-')
    and 'adoptium' not in b[1].lower()
    and 'jdk' not in b[1].lower()
    and 'windows kits' not in b[1].lower()
    and b[0].lower() != 'ucrtbase.dll'
]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WAV-Ripper',
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
    icon=['logo.ico'],
)
