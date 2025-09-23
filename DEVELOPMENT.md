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
- ✅ **Manual Milestone Capture**: Screenshots + text note on demand
- ✅ **Toggle Auto Screenshots**: Enable/disable automatic mode
- ✅ **Time Display**: Menu bar shows last capture time
- ✅ **Organized Storage**: Files saved in `~/Documents/mac-cappy/`
  - Auto Screenshots: `~/Documents/mac-cappy/Captures/YYYY-MM-DD/*-auto-screen-*.png`
  - Milestone Screenshots: `~/Documents/mac-cappy/Captures/YYYY-MM-DD/*-milestone-screen-*.png`
  - Logs: `~/Documents/mac-cappy/Logs/YYYY-MM-DD/*-milestone.md`
- ✅ **Debug Menu**: "Debug: Open Log Folder" for easy access
- ✅ **Improved Error Handling**: Better user feedback for common issues

### Menu Options
1. **Manual Capture + Note**: Takes screenshots + prompts for milestone note
2. **Auto Screenshots: ON/OFF**: Toggle automatic screenshot mode (60-second interval)
3. **Check Permissions**: Test and fix screen recording permissions
4. **Debug: Open Log Folder**: Opens logs directory in Finder

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
- [ ] Manual milestone capture works (screenshots + note dialog)
- [ ] Toggle auto screenshots on/off works
- [ ] Files save to correct locations with proper naming
- [ ] Debug menu opens Finder
- [ ] Error handling works (try without screen recording permission)
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