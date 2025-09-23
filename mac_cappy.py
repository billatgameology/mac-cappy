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

def check_screen_recording_permission():
    """Check if screen recording permission is granted."""
    try:
        # Try to take a small test screenshot
        with mss.mss() as sct:
            # Capture a small area from the main monitor
            if len(sct.monitors) > 1:
                monitor = sct.monitors[1]
                test_area = {
                    'top': monitor['top'], 
                    'left': monitor['left'], 
                    'width': 100, 
                    'height': 100
                }
                img = sct.grab(test_area)
                # If we can grab and the image has content, permission is likely granted
                return True
    except Exception as e:
        print(f"Permission check failed: {e}")
        return False

def take_screenshot_with_screencapture(output_path, display_number=1):
    """Alternative screenshot method using macOS screencapture command."""
    try:
        # Use macOS built-in screencapture command
        cmd = ["screencapture", "-D", str(display_number), "-x", output_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"screencapture failed: {e}")
        return False 

class MacCappyApp(rumps.App):
    def __init__(self):
        super(MacCappyApp, self).__init__(APP_NAME, icon=None, title=APP_ICON)
        self.menu = [
            "Manual Capture + Note", 
            "---", 
            rumps.MenuItem("Auto Screenshots: ON", callback=self.toggle_auto_screenshots),
            "---",
            "Check Permissions",
            "Debug: Open Log Folder", 
            "---"
        ]
        
        # Ensure base directories exist
        try:
            os.makedirs(CAPTURES_DIR, exist_ok=True)
            os.makedirs(LOGS_DIR, exist_ok=True)
        except Exception as e:
            rumps.alert(title="Setup Error", message=f"Failed to create directories: {e}")
        
        # Check permissions on startup
        if not check_screen_recording_permission():
            rumps.notification(
                title=APP_NAME,
                subtitle="Permission Required",
                message="Click 'Check Permissions' to enable screen recording"
            )
        
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
            
            # Capture screenshots silently
            screenshot_count = 0
            with mss.mss() as sct:
                if len(sct.monitors) > 1:
                    for i, monitor in enumerate(sct.monitors[1:], 1):
                        filename = os.path.join(today_captures_dir, f"{time_filename_base}-auto-screen-{i}.png")
                        sct.shot(mon=i, output=filename)
                        screenshot_count += 1
                        
                        # Check if screenshot captured actual content
                        if os.path.exists(filename):
                            file_size = os.path.getsize(filename)
                            if file_size < 1000:  # Very small file suggests permission issue
                                print(f"Warning: Screenshot {filename} is unusually small ({file_size} bytes)")
            
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
        
        # 2. Capture screenshots of all monitors
        screenshot_paths = []
        try:
            with mss.mss() as sct:
                # Check if we have any monitors
                if len(sct.monitors) <= 1:
                    rumps.alert(title="Monitor Error", message="No monitors detected for screenshot capture.")
                    return
                    
                for i, monitor in enumerate(sct.monitors[1:], 1): # sct.monitors[0] is all screens
                    filename = os.path.join(today_captures_dir, f"{time_filename_base}-milestone-screen-{i}.png")
                    
                    # Try MSS first, then fallback to screencapture
                    try:
                        sct.shot(mon=i, output=filename)
                        # Check if file is reasonable size
                        if os.path.exists(filename) and os.path.getsize(filename) < 1000:
                            # File too small, try screencapture instead
                            if take_screenshot_with_screencapture(filename, i):
                                print(f"Used screencapture fallback for monitor {i}")
                    except:
                        # MSS failed, try screencapture
                        if take_screenshot_with_screencapture(filename, i):
                            print(f"MSS failed, used screencapture for monitor {i}")
                    
                    if os.path.exists(filename):
                        screenshot_paths.append(filename)
                    
            if screenshot_paths:
                rumps.notification(
                    title=APP_NAME,
                    subtitle="Screenshots Captured!",
                    message=f"Saved {len(screenshot_paths)} screen(s). Now, add your note."
                )
            else:
                rumps.alert(title="Screenshot Error", message="Failed to capture any screenshots. Check permissions.")
                return
        except Exception as e:
            rumps.alert(title="Screenshot Error", message=f"Failed to capture screens: {e}\n\nTry clicking 'Check Permissions' to resolve this issue.")
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

    @rumps.clicked("Check Permissions")
    def check_permissions(self, _):
        """Check and guide user through screen recording permissions."""
        try:
            # Test screenshot capability
            with mss.mss() as sct:
                if len(sct.monitors) > 1:
                    # Try to capture a test screenshot
                    monitor = sct.monitors[1]
                    test_filename = os.path.join(CAPTURES_DIR, "permission_test.png")
                    sct.shot(mon=1, output=test_filename)
                    
                    # Check if file was created and has reasonable size
                    if os.path.exists(test_filename):
                        file_size = os.path.getsize(test_filename)
                        os.remove(test_filename)  # Clean up test file
                        
                        if file_size > 1000:  # Reasonable screenshot size
                            rumps.alert(
                                title="Permissions OK", 
                                message="Screen recording permissions appear to be working correctly!"
                            )
                            return
                        else:
                            # File too small, likely just background
                            raise Exception("Screenshot only captured background")
                    else:
                        raise Exception("Failed to create screenshot file")
                        
        except Exception as e:
            # Permission issue detected
            rumps.alert(
                title="Screen Recording Permission Required",
                message="""mac-cappy needs Screen Recording permission to capture application windows.

Please:
1. Open System Preferences/Settings
2. Go to Security & Privacy → Privacy → Screen Recording
3. Add and enable 'Python' or 'Terminal'
4. Restart mac-cappy

Current issue: Only capturing desktop background, not application windows."""
            )
            
            # Open System Preferences to the right location
            subprocess.run([
                "open", 
                "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
            ])

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