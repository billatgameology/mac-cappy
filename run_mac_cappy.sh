#!/bin/bash

# mac-cappy runner script
# Activates virtual environment and runs the application

cd "$(dirname "$0")"
source venv/bin/activate

# Ensure Info.plist exists for rumps notifications
PLIST_PATH="venv/bin/Info.plist"
if [ ! -f "$PLIST_PATH" ]; then
    echo "Creating Info.plist for rumps notifications..."
    /usr/libexec/PlistBuddy -c 'Add :CFBundleIdentifier string "rumps"' "$PLIST_PATH" 2>/dev/null
    /usr/libexec/PlistBuddy -c 'Add :CFBundleName string "mac-cappy"' "$PLIST_PATH" 2>/dev/null
    /usr/libexec/PlistBuddy -c 'Add :CFBundleVersion string "1.0"' "$PLIST_PATH" 2>/dev/null
fi

python mac_cappy.py