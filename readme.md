Copilot Instructions: Build a Python macOS Milestone Logger
Project Goal: Create a simple, lightweight macOS menu bar application called mac-cappy. This app will run in the background and allow me to manually capture "milestones." A milestone consists of screenshots and a text note, which are saved as a unique Markdown file inside a folder for the current day.

Core Technologies:

Python 3

rumps library: For creating the native macOS menu bar interface.

mss library: For taking multi-monitor screenshots.

py2app: For packaging the final script into a standalone .app file.

Phase 1: Project Setup
Instructions: Please execute these commands in my VS Code terminal to set up the project environment.

Create a new project folder and navigate into it.

mkdir mac-cappy-app && cd mac-cappy-app

Create a Python virtual environment.

python3 -m venv venv

Activate the virtual environment.

source venv/bin/activate

Install the required Python libraries.

pip install rumps mss py2app

Create the main Python script file.

touch mac_cappy.py

Phase 2: Write the Core Application Logic
Instructions: Please open the mac_cappy.py file and populate it with the following Python code.

import rumps
import mss
import os
from datetime import datetime

# --- Configuration ---
APP_NAME = "mac-cappy"
BASE_DIR = os.path.expanduser(f"~/Documents/{APP_NAME}")
CAPTURES_DIR = os.path.join(BASE_DIR, "Captures")
LOGS_DIR = os.path.join(BASE_DIR, "Logs")
APP_ICON = "📸" 

class MacCappyApp(rumps.App):
    def __init__(self):
        super(MacCappyApp, self).__init__(APP_NAME, icon=None, title=APP_ICON)
        self.menu = ["Capture Milestone", "---", "Quit"]
        # Ensure base directories exist
        os.makedirs(CAPTURES_DIR, exist_ok=True)
        os.makedirs(LOGS_DIR, exist_ok=True)

    @rumps.clicked("Capture Milestone")
    def capture_milestone(self, _):
        """Takes screenshots, asks for a note, and saves to a new log file."""
        timestamp = datetime.now()
        date_folder = timestamp.strftime("%Y-%m-%d")
        time_filename_base = timestamp.strftime("%H-%M-%S")
        
        # 1. Create directory for today's captures and logs
        today_captures_dir = os.path.join(CAPTURES_DIR, date_folder)
        today_logs_dir = os.path.join(LOGS_DIR, date_folder)
        os.makedirs(today_captures_dir, exist_ok=True)
        os.makedirs(today_logs_dir, exist_ok=True)
        
        # 2. Capture screenshots of all monitors
        screenshot_paths = []
        try:
            with mss.mss() as sct:
                for i, monitor in enumerate(sct.monitors[1:], 1): # sct.monitors[0] is all screens
                    filename = os.path.join(today_captures_dir, f"{time_filename_base}-screen-{i}.png")
                    sct.shot(mon=i, output=filename)
                    screenshot_paths.append(filename)
            rumps.notification(
                title=APP_NAME,
                subtitle="Screenshots Captured!",
                message=f"Saved {len(screenshot_paths)} screen(s). Now, add your note."
            )
        except Exception as e:
            rumps.alert(title="Screenshot Error", message=f"Failed to capture screens: {e}")
            return

        # 3. Ask for a developer note
        window = rumps.Window(
            message="What was the breakthrough or milestone you just reached?",
            title="Add Developer Note",
            ok="Save Milestone",
            cancel="Cancel"
        )
        response = window.run()

        # 4. Save the log entry to a new file if the user provided text
        if response.clicked and response.text:
            note = response.text
            log_content = self.format_log_entry(timestamp, note, screenshot_paths)
            log_filename = f"{time_filename_base}.md"
            log_filepath = os.path.join(today_logs_dir, log_filename)
            
            with open(log_filepath, "w") as f:
                f.write(log_content)
            
            rumps.notification(
                title=APP_NAME,
                subtitle="Milestone Saved!",
                message=f"Log saved to {log_filename}"
            )
        else:
             rumps.notification(
                title=APP_NAME,
                subtitle="Capture Canceled",
                message="The milestone was not saved."
            )

    def format_log_entry(self, timestamp, note, image_paths):
        """Formats the milestone into a Markdown string for a new file."""
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        # Create markdown links for each image using absolute paths
        image_links = ""
        for i, path in enumerate(image_paths):
            image_links += f"![Screen {i+1}]({os.path.abspath(path)})\n"
            
        return f"""
# Milestone: {formatted_timestamp}

{note}

---

## Captures

{image_links}
"""

    @rumps.clicked("Quit")
    def quit_app(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    MacCappyApp().run()

Phase 3: Prepare for Packaging
Instructions: Now, create a setup.py file in the root directory.

touch setup.py

Instructions: Open setup.py and populate it with the following code. Note that we've updated the APP variable to use the new script name.

from setuptools import setup

APP = ['mac_cappy.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'LSUIElement': True, # This makes it a background-only app
    },
    'packages': ['rumps', 'mss'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

Instructions: Create a placeholder icon file.

touch icon.icns

Phase 4: Build and Run the Application
Instructions: Now, run the py2app command to build the .app file.

python3 setup.py py2app
