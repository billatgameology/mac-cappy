from setuptools import setup
import sys
import os

# Find libffi.8.dylib in common locations
def find_libffi():
    """Find libffi.8.dylib in common macOS locations"""
    possible_paths = [
        '/opt/anaconda3/lib/libffi.8.dylib',
        '/usr/local/lib/libffi.8.dylib',
        '/opt/homebrew/lib/libffi.8.dylib',
        '/usr/lib/libffi.8.dylib',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If not found, try to find it relative to Python
    python_lib = os.path.dirname(sys.executable)
    anaconda_lib = os.path.join(os.path.dirname(python_lib), 'lib', 'libffi.8.dylib')
    if os.path.exists(anaconda_lib):
        return anaconda_lib
    
    raise FileNotFoundError(
        "Could not find libffi.8.dylib. Please install it via:\n"
        "  brew install libffi\n"
        "or ensure your Python environment includes it."
    )

APP = ['mac_cappy.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'LSUIElement': True,  # This makes it a background-only app
        'CFBundleName': 'mac-cappy',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.github.billatgameology.mac-cappy',
    },
    'packages': ['rumps', 'mss'],
    'frameworks': [find_libffi()],
    'excludes': ['setuptools', 'pkg_resources'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)