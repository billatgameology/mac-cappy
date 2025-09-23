import rumps
import mss
import os
import subprocess
import threading
import time
from datetime import datetime

# --- Configuration ---
APP_NAME = "mac-cappy"
BASE_DIR = os.path.expanduser(f"~/Documents/{APP_NAME}")
CAPTURES_DIR = os.path.join(BASE_DIR, "Captures")
LOGS_DIR = os.path.join(BASE_DIR, "Logs")
APP_ICON = "📸"
SCREENSHOT_INTERVAL = 60  # seconds 

class MacCappyApp(rumps.App):
    def __init__(self):
        super(MacCappyApp, self).__init__(APP_NAME, icon=None, title=APP_ICON)
        self.menu = [
            "Manual Capture + Note", 
            "---", 
            rumps.MenuItem("Auto Screenshots: ON", callback=self.toggle_auto_screenshots),
            "---",
            "Debug: Open Log Folder", 
            "---"
        ]
        
        # Ensure base directories exist
        try:
            os.makedirs(CAPTURES_DIR, exist_ok=True)
            os.makedirs(LOGS_DIR, exist_ok=True)
        except Exception as e:
            rumps.alert(title="Setup Error", message=f"Failed to create directories: {e}")
        
        # Auto-screenshot functionality
        self.auto_screenshots_enabled = True
        self.screenshot_timer = None
        self.start_auto_screenshots()

    def start_auto_screenshots(self):
        """Start the automatic screenshot timer."""
        if self.auto_screenshots_enabled and self.screenshot_timer is None:
            self.screenshot_timer = rumps.Timer(self.take_auto_screenshot, SCREENSHOT_INTERVAL)
            self.screenshot_timer.start()
    
    def stop_auto_screenshots(self):
        """Stop the automatic screenshot timer."""
        if self.screenshot_timer:
            self.screenshot_timer.stop()
            self.screenshot_timer = None
    
    def take_auto_screenshot(self, sender):
        """Take automatic screenshots without user interaction."""
        try:
            timestamp = datetime.now()
            date_folder = timestamp.strftime("%Y-%m-%d")
            time_filename_base = timestamp.strftime("%H-%M-%S")
            
            # Create directory for today's captures
            today_captures_dir = os.path.join(CAPTURES_DIR, date_folder)
            os.makedirs(today_captures_dir, exist_ok=True)
            
            # Capture screenshots silently - SIMPLE VERSION LIKE ORIGINAL
            screenshot_count = 0
            with mss.mss() as sct:
                for i, monitor in enumerate(sct.monitors[1:], 1):
                    filename = os.path.join(today_captures_dir, f"{time_filename_base}-auto-screen-{i}.png")
                    sct.shot(mon=i, output=filename)
                    screenshot_count += 1
            
            # Update menu bar title to show last capture time
            self.title = f"📸 {timestamp.strftime('%H:%M')}"
            
        except Exception as e:
            # Silent failure for auto-screenshots to avoid interrupting user
            print(f"Auto-screenshot failed: {e}")
    
    @rumps.clicked("Auto Screenshots: ON")
    def toggle_auto_screenshots(self, sender):
        """Toggle automatic screenshot functionality."""
        self.auto_screenshots_enabled = not self.auto_screenshots_enabled
        
        if self.auto_screenshots_enabled:
            sender.title = "Auto Screenshots: ON"
            self.start_auto_screenshots()
            rumps.notification(
                title=APP_NAME,
                subtitle="Auto Screenshots Enabled",
                message=f"Taking screenshots every {SCREENSHOT_INTERVAL} seconds"
            )
        else:
            sender.title = "Auto Screenshots: OFF"
            self.stop_auto_screenshots()
            self.title = APP_ICON  # Reset title
            rumps.notification(
                title=APP_NAME,
                subtitle="Auto Screenshots Disabled",
                message="Manual capture only"
            )

    @rumps.clicked("Manual Capture + Note")
    def capture_milestone(self, _):
        """Takes screenshots, asks for a note, and saves to a new log file."""
        timestamp = datetime.now()
        date_folder = timestamp.strftime("%Y-%m-%d")
        time_filename_base = timestamp.strftime("%H-%M-%S")
        
        # 1. Create directory for today's captures and logs
        today_captures_dir = os.path.join(CAPTURES_DIR, date_folder)
        today_logs_dir = os.path.join(LOGS_DIR, date_folder)
        
        try:
            os.makedirs(today_captures_dir, exist_ok=True)
            os.makedirs(today_logs_dir, exist_ok=True)
        except Exception as e:
            rumps.alert(title="Directory Error", message=f"Failed to create today's folders: {e}")
            return
        
        # 2. Capture screenshots of all monitors - SIMPLE VERSION LIKE ORIGINAL
        screenshot_paths = []
        try:
            with mss.mss() as sct:
                for i, monitor in enumerate(sct.monitors[1:], 1): # sct.monitors[0] is all screens
                    filename = os.path.join(today_captures_dir, f"{time_filename_base}-milestone-screen-{i}.png")
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
        if response.clicked and response.text.strip():
            note = response.text.strip()
            log_content = self.format_log_entry(timestamp, note, screenshot_paths)
            log_filename = f"{time_filename_base}-milestone.md"
            log_filepath = os.path.join(today_logs_dir, log_filename)
            
            try:
                with open(log_filepath, "w", encoding="utf-8") as f:
                    f.write(log_content)
                
                rumps.notification(
                    title=APP_NAME,
                    subtitle="Milestone Saved!",
                    message=f"Log saved to {log_filename}"
                )
            except Exception as e:
                rumps.alert(title="Save Error", message=f"Failed to save log file: {e}\n\nThis might be a permissions issue with the Documents folder.")
        else:
             rumps.notification(
                title=APP_NAME,
                subtitle="Capture Canceled",
                message="The milestone was not saved."
            )

    @rumps.clicked("Debug: Open Log Folder")
    def open_log_folder(self, _):
        """Opens the logs directory in Finder for easy access during development."""
        try:
            if os.path.exists(LOGS_DIR):
                subprocess.run(["open", LOGS_DIR])
                rumps.notification(
                    title=APP_NAME,
                    subtitle="Folder Opened",
                    message="Logs folder opened in Finder"
                )
            else:
                # Create the directory first, then open it
                os.makedirs(LOGS_DIR, exist_ok=True)
                subprocess.run(["open", LOGS_DIR])
                rumps.notification(
                    title=APP_NAME,
                    subtitle="Folder Created & Opened",
                    message="Created and opened logs folder in Finder"
                )
        except Exception as e:
            rumps.alert(title="Folder Error", message=f"Failed to open logs folder: {e}")

    def format_log_entry(self, timestamp, note, image_paths):
        """Formats the milestone into a Markdown string for a new file."""
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        # Create markdown links for each image using relative paths for better portability
        image_links = ""
        for i, path in enumerate(image_paths, 1):
            # Get relative path from logs directory to captures directory
            rel_path = os.path.relpath(path, os.path.dirname(os.path.dirname(path)))
            image_links += f"![Screen {i}]({rel_path})\n\n"
            
        return f"""# Milestone: {formatted_timestamp}

{note}

---

## Captures

{image_links}---

*Captured with mac-cappy*
"""

    def quit_application(self):
        """Clean shutdown of the application."""
        self.stop_auto_screenshots()
        rumps.quit_application()

if __name__ == "__main__":
    MacCappyApp().run()