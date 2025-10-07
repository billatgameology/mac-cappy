# mac-cappy 📸# mac-cappy 📸Copilot Instructions: Build a Python macOS Milestone Logger



Capture your work progress automatically. Mac-cappy is a lightweight macOS menu bar app that takes screenshots of your workflow every minute, helping you create time-lapses, track your progress, or document what you've been working on.Project Goal: Create a simple, lightweight macOS menu bar application called mac-cappy. This app will run in the background and allow me to manually capture screenshots.



## What It DoesA lightweight macOS menu bar app that automatically captures screenshots of your development workflow every 60 seconds, with intelligent duplicate detection to skip idle time.



Mac-cappy sits quietly in your menu bar and automatically captures screenshots every 60 seconds. It's smart enough to skip captures when nothing on your screen has changed, so you don't end up with hundreds of identical images when you step away from your computer.Core Technologies:



Perfect for:Perfect for creating time-lapses of your coding sessions, tracking your progress, or documenting your development process.

- Creating time-lapse videos of your work

- Tracking how you spend your timePython 3

- Documenting your workflow

- Reviewing what you accomplished during the day## Features



## Key Featuresrumps library: For creating the native macOS menu bar interface.



- **Automatic Capture**: Takes screenshots every 60 seconds without you having to remember- 🔄 **Auto Screenshots**: Captures screens every 60 seconds

- **Smart Idle Detection**: Skips duplicate screenshots when your screen hasn't changed (ignores your menu bar and clock)

- **Manual Capture**: Click to take a screenshot anytime you want- 🧠 **Smart Idle Detection**: Skips duplicate screenshots when nothing changes (ignores clock/menubar)mss library: For taking multi-monitor screenshots.

- **Activity Counter**: See how many screenshots were skipped due to idle time and how many manual captures you've taken

- **Multi-Monitor Support**: Captures all connected displays at once- 📊 **Activity Tracking**: Counts idle skips and manual captures

- **Organized Storage**: Screenshots are automatically sorted by date into folders

- **Privacy First**: Everything stays on your Mac—no cloud uploads, no tracking, no data sent anywhere- 👆 **Manual Capture**: Take screenshots on demandpy2app: For packaging the final script into a standalone .app file.



## Download & Install- 🗂️ **Organized Storage**: Screenshots saved by date (YYYY-MM-DD)



**[Download latest release](https://github.com/billatgameology/mac-cappy/releases/latest)**- 🖥️ **Multi-Monitor**: Captures all connected displaysPhase 1: Project Setup



1. Download `mac-cappy.zip` from the releases page- 🚫 **No Dock Icon**: Runs quietly in the menu barInstructions: Please execute these commands in my VS Code terminal to set up the project environment.

2. Unzip the file

3. Drag `mac-cappy.app` to your Applications folder

4. Double-click to launch (you'll see 📸 appear in your menu bar)

## DownloadCreate a new project folder and navigate into it.

### Important: Grant Screen Recording Permission



When you first launch mac-cappy, macOS will ask for permission to record your screen. This is required for the app to capture screenshots.

**[Download latest release](https://github.com/billatgameology/mac-cappy/releases/latest)**mkdir mac-cappy-app && cd mac-cappy-app

**Setup Steps:**



1. Launch mac-cappy (you'll see 📸 in your menu bar)

2. macOS will prompt you about Screen Recording access1. Download `mac-cappy.zip`Create a Python virtual environment.

3. Click "Open System Settings"

4. In System Settings, navigate to: **Privacy & Security → Screen Recording**2. Unzip and move `mac-cappy.app` to your Applications folder

5. Find "mac-cappy" in the list and toggle it **ON**

6. **Important**: Quit and restart mac-cappy for the permission to take effect3. Launch the app (you'll see 📸 in your menu bar)python3 -m venv venv



**If you don't see the permission prompt:**4. Grant **Screen Recording** permission when prompted:

- Open **System Settings** manually

- Go to **Privacy & Security → Screen Recording**   - System Settings → Privacy & Security → Screen RecordingActivate the virtual environment.

- Click the **+** button and add mac-cappy from your Applications folder

- Toggle it **ON**   - Enable mac-cappy

- Restart mac-cappy

source venv/bin/activate

## Where Are My Screenshots?

## Screenshots Storage

Your screenshots are saved to:

Install the required Python libraries.

```

~/Documents/mac-cappy/Captures/YYYY-MM-DD/Screenshots are saved to: `~/Documents/mac-cappy/Captures/YYYY-MM-DD/`

```

pip install rumps mss py2app

Each day gets its own folder with screenshots named by timestamp. For example:

Example:

```

Documents/mac-cappy/Captures/```Create the main Python script file.

  └── 2025-10-06/

      ├── 14-30-00-screen-1.png~/Documents/mac-cappy/Captures/

      ├── 14-31-00-screen-1.png

      └── 14-32-00-screen-1.png  └── 2025-10-06/touch mac_cappy.py

```

      ├── 14-30-00-screen-1.png

## Using Mac-cappy

      ├── 14-31-00-screen-1.pngPhase 2: Write the Core Application Logic

Click the 📸 icon in your menu bar to see:

      └── 14-32-00-screen-1.pngInstructions: Please open the mac_cappy.py file and populate it with the following Python code.

- **Auto Screenshots: ON/OFF** - Turn automatic capture on or off

- **Idle Skips** - How many duplicate screenshots were skipped```

- **Manual Captures** - How many times you manually captured

- **Manual Capture** - Take a screenshot right nowimport rumps

- **Open Today's Captures** - Opens today's screenshot folder in Finder

- **Quit** - Stop the app## Building from Sourceimport mss



## Privacy & Securityimport os



- All screenshots are stored **locally on your Mac**### Requirementsfrom datetime import datetime

- Nothing is uploaded to any server or cloud service

- No analytics, tracking, or telemetry of any kind- macOS 11.0+

- Open source code—you can review everything yourself

- Python 3.12+# --- Configuration ---

## License

- libffi.8.dylib (included with Anaconda or install via Homebrew)APP_NAME = "mac-cappy"

MIT License - see [LICENSE](LICENSE) file

BASE_DIR = os.path.expanduser(f"~/Documents/{APP_NAME}")

## Contributing

### SetupCAPTURES_DIR = os.path.join(BASE_DIR, "Captures")

Found a bug or have a feature request? Open an issue or submit a pull request on [GitHub](https://github.com/billatgameology/mac-cappy).

LOGS_DIR = os.path.join(BASE_DIR, "Logs")

## Troubleshooting

```bashAPP_ICON = "📸" 

**The app captures my desktop but not my windows:**

- Make sure you've granted Screen Recording permission in System Settings# Clone the repository

- After granting permission, **fully quit and restart** mac-cappy

git clone https://github.com/billatgameology/mac-cappy.gitclass MacCappyApp(rumps.App):

**The app won't launch:**

- Check Screen Recording permission in System Settings → Privacy & Securitycd mac-cappy    def __init__(self):

- Make sure macOS didn't block the app (right-click and choose "Open" the first time)

        super(MacCappyApp, self).__init__(APP_NAME, icon=None, title=APP_ICON)

**Need more help?**

- Check the [Issues](https://github.com/billatgameology/mac-cappy/issues) page on GitHub# Create virtual environment        self.menu = ["Capture Milestone", "---", "Quit"]

- Open a new issue with details about your problem

python3 -m venv venv        # Ensure base directories exist

source venv/bin/activate        os.makedirs(CAPTURES_DIR, exist_ok=True)

        os.makedirs(LOGS_DIR, exist_ok=True)

# Install dependencies

pip install rumps mss py2app    @rumps.clicked("Capture Milestone")

    def capture_milestone(self, _):

# Build the app        """Takes screenshots, asks for a note, and saves to a new log file."""

python setup.py py2app        timestamp = datetime.now()

        date_folder = timestamp.strftime("%Y-%m-%d")

# The app will be in dist/mac-cappy.app        time_filename_base = timestamp.strftime("%H-%M-%S")

```        

        # 1. Create directory for today's captures and logs

### If libffi is missing        today_captures_dir = os.path.join(CAPTURES_DIR, date_folder)

        today_logs_dir = os.path.join(LOGS_DIR, date_folder)

```bash        os.makedirs(today_captures_dir, exist_ok=True)

# Install via Homebrew        os.makedirs(today_logs_dir, exist_ok=True)

brew install libffi        

```        # 2. Capture screenshots of all monitors

        screenshot_paths = []

## Development        try:

            with mss.mss() as sct:

Run from source without building:                for i, monitor in enumerate(sct.monitors[1:], 1): # sct.monitors[0] is all screens

                    filename = os.path.join(today_captures_dir, f"{time_filename_base}-screen-{i}.png")

```bash                    sct.shot(mon=i, output=filename)

source venv/bin/activate                    screenshot_paths.append(filename)

python mac_cappy.py            rumps.notification(

```                title=APP_NAME,

                subtitle="Screenshots Captured!",

See [DEVELOPMENT.md](DEVELOPMENT.md) for more details.                message=f"Saved {len(screenshot_paths)} screen(s). Now, add your note."

            )

## How It Works        except Exception as e:

            rumps.alert(title="Screenshot Error", message=f"Failed to capture screens: {e}")

1. **Auto Screenshots**: Every 60 seconds, captures all monitors            return

2. **Duplicate Detection**: Compares MD5 hash of the bottom 90% of screen (excluding menu bar/clock)

3. **Skip Idle Time**: If hash matches previous screenshot, skips saving and increments idle counter        # 3. Ask for a developer note

4. **Manual Override**: Click "Manual Capture" anytime to force a screenshot        window = rumps.Window(

            message="What was the breakthrough or milestone you just reached?",

## Menu Options            title="Add Developer Note",

            ok="Save Milestone",

- **Auto Screenshots: ON/OFF** - Toggle automatic capture            cancel="Cancel"

- **Idle Skips: N** - Shows how many duplicate screenshots were skipped        )

- **Manual Captures: N** - Counts manual screenshots taken        response = window.run()

- **Manual Capture** - Take a screenshot immediately

- **Debug: Open Today's Captures** - Opens today's screenshot folder in Finder        # 4. Save the log entry to a new file if the user provided text

        if response.clicked and response.text:

## Privacy            note = response.text

            log_content = self.format_log_entry(timestamp, note, screenshot_paths)

- All screenshots are stored **locally** on your Mac            log_filename = f"{time_filename_base}.md"

- No data is sent to any server            log_filepath = os.path.join(today_logs_dir, log_filename)

- No analytics or tracking            

- Open source - audit the code yourself!            with open(log_filepath, "w") as f:

                f.write(log_content)

## License            

            rumps.notification(

MIT License - see [LICENSE](LICENSE) file                title=APP_NAME,

                subtitle="Milestone Saved!",

## Credits                message=f"Log saved to {log_filename}"

            )

Built with:        else:

- [rumps](https://github.com/jaredks/rumps) - macOS menu bar framework             rumps.notification(

- [mss](https://github.com/BoboTiG/python-mss) - Fast screenshot library                title=APP_NAME,

                subtitle="Capture Canceled",

## Contributing                message="The milestone was not saved."

            )

Issues and pull requests welcome!

    def format_log_entry(self, timestamp, note, image_paths):