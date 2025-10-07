# mac-cappy Development Guide

## Quick Start

### Running the Application
```bash
./run_mac_cappy.sh
```

Or manually:
```bash
source venv/bin/activate
python mac_cappy.py
```

### Features Implemented
- ✅ **Menu Bar Interface**: Camera emoji (📸) appears in menu bar
- ✅ **Automatic Screenshots**: Takes screenshots every 60 seconds automatically
- ✅ **Smart Duplicate Detection**: Compares screenshots before saving to avoid idle duplicates
- ✅ **Clock-Aware Coverage**: Excludes top 10% of screen (90% coverage) to avoid menu bar/clock changes  
- ✅ **High-Resolution Support**: Works with ultrawide and high-DPI displays
- ✅ **Idle Skip Counter**: Shows how many duplicate screenshots were skipped
- ✅ **Manual Capture**: One-click screenshot capture without note prompts
- ✅ **Manual Capture Counter**: Tracks total manual captures taken
- ✅ **Toggle Auto Screenshots**: Enable/disable automatic mode
- ✅ **Time Display**: Menu bar shows last capture time (with skip indicator)
- ✅ **Memory Efficient**: Screenshot comparison done in memory using MD5 hashes
- ✅ **Organized Storage**: Files saved in `~/Documents/mac-cappy/Captures/YYYY-MM-DD/`
  - Auto Screenshots: `*-auto-screen-*.png`
  - Manual Screenshots: `*-manual-screen-*.png`
- ✅ **Quick Access**: Debug menu opens today's capture folder in Finder

### Menu Options
1. **Manual Capture**: Takes screenshots immediately without note prompt
2. **Auto Screenshots: ON/OFF**: Toggle automatic screenshot mode (60-second interval)
3. **Idle Skips: X**: Shows count of duplicate screenshots skipped (resets on toggle)
4. **Manual Captures: X**: Shows total count of manual captures taken (resets on app restart)
5. **Debug: Open Today's Captures**: Opens today's capture folder in Finder

### File Structure
```
mac-cappy/
├── mac_cappy.py          # Main application
├── setup.py              # py2app build configuration
├── run_mac_cappy.sh      # Quick run script
├── venv/                 # Virtual environment
├── .gitignore           # Git ignore rules
└── readme.md            # Original instructions
```

### Building Standalone App
```bash
source venv/bin/activate
python setup.py py2app
```

The built app will be in `dist/mac_cappy.app`

### Improvements Made
1. **Removed icon dependency** - Uses emoji only for simplicity
2. **Added debug menu** - Easy access to log folder
3. **Better error handling** - More specific error messages
4. **Relative image paths** - Better portability of markdown files
5. **Enhanced notifications** - Clearer user feedback
6. **Input validation** - Checks for empty notes

### Testing Checklist
- [ ] Menu bar icon appears (📸)
- [ ] Auto screenshots start immediately (every 60 seconds)
- [ ] Menu bar title updates with last capture time (📸 HH:MM)
- [ ] Duplicate detection works with 90% screen coverage (excludes top 10%)
- [ ] Works properly with ultrawide/high-resolution displays
- [ ] Leave computer idle for 2+ minutes - should see skip counter increment
- [ ] Menu shows "📸 HH:MM (skip)" when duplicates detected
- [ ] "Idle Skips: X" counter increments when duplicates found
- [ ] Skip counter resets to 0 when toggling auto screenshots
- [ ] Manual capture works (no note prompt, just takes screenshots)
- [ ] "Manual Captures: X" counter increments with each manual capture
- [ ] Manual counter resets to 0 when app restarts
- [ ] Toggle auto screenshots on/off works
- [ ] Files save to correct locations with proper naming (*-auto-*.png, *-manual-*.png)
- [ ] "Debug: Open Today's Captures" opens correct folder
- [ ] App quits cleanly (stops auto timer)

### Common Issues
- **Only capturing background**: Click "Check Permissions" → Enable Screen Recording for Python/Terminal
- **Permission Error**: Enable "Screen Recording" permission in System Preferences > Security & Privacy
- **rumps notification error**: Fixed automatically by run script (creates Info.plist)
- **Build Errors**: Try `python setup.py py2app --alias` for faster development builds
- **Menu Bar Missing**: Check if another instance is already running

### Screenshot Permission Fix
If screenshots only show desktop background (no app windows):

1. **Click "Check Permissions"** in mac-cappy menu - this will:
   - Test screenshot capability
   - Open System Preferences automatically
   - Show detailed guidance

2. **Manual steps**:
   - Open System Preferences/Settings
   - Go to Security & Privacy → Privacy → Screen Recording  
   - Add and enable 'Python' or 'Terminal'
   - Restart mac-cappy

3. **Technical details**:
   - App uses dual screenshot methods: `mss` library + `screencapture` fallback
   - Automatic size checking detects permission issues
   - Files under 1KB usually indicate background-only capture

### Next Steps
- Add app icon (.icns file)
- Implement milestone browsing/searching
- Add export functionality
- Create installer package