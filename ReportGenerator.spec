# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_all

# Recolectar PySide6 completo
datas = [('iconos', 'iconos')]
binaries = []
hiddenimports = []

pyside_datas, pyside_bins, pyside_hidden = collect_all('PySide6')
datas += pyside_datas
binaries += pyside_bins
hiddenimports += pyside_hidden

# Archivo de versión PE
version_file = os.path.join(os.path.dirname(__name__), 'version_info.txt')

a = Analysis(
    ['src/main_UI.py'],
    pathex=[os.path.abspath('src')],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ReportGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    icon='iconos/app_imag.ico',
    version=version_file,
)