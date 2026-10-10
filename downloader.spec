import sys
import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

ct_datas, ct_binaries, ct_hiddenimports = collect_all('customtkinter')
ytdlp_datas, ytdlp_binaries, ytdlp_hiddenimports = collect_all('yt_dlp')

ejs_datas, ejs_binaries, ejs_hiddenimports = collect_all('yt_dlp_ejs')

exe_ext = '.exe' if sys.platform == 'win32' else ''
extra_binaries = []
for tool in ('ffmpeg', 'deno'):
    src = os.path.join('bin', tool + exe_ext)
    if os.path.isfile(src):
        extra_binaries.append((src, 'bin'))

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=ct_binaries + ytdlp_binaries + ejs_binaries + extra_binaries,
    datas=ct_datas + ytdlp_datas + ejs_datas,
    hiddenimports=ct_hiddenimports + ytdlp_hiddenimports + ejs_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='YT-MP3-Downloader',
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
    name='YT-MP3-Downloader',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='YT-MP3-Downloader.app',
        bundle_identifier='com.ytmp3downloader.app',
        info_plist={
            'NSHighResolutionCapable': True,
        },
    )
