import rumps
import mss
import os
import subprocess
import threading
import time
import hashlib
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
        
        # Initialize skip counter and previous screenshot hashes
        self.idle_skip_count = 0
        self.previous_screenshot_hashes = {}  # monitor_id -> hash
        
        # Create menu items with references
        self.auto_toggle_item = rumps.MenuItem("Auto Screenshots: ON", callback=self.toggle_auto_screenshots)
        self.skip_counter_item = rumps.MenuItem("Idle Skips: 0", callback=None)
        
        self.menu = [
            "Manual Capture + Note", 
            "---", 
            self.auto_toggle_item,
            self.skip_counter_item,
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
    
    def get_screenshot_hash(self, sct, monitor_id):
        """Get a hash of the screenshot for comparison without saving to disk.
        Uses multiple small sample areas to avoid clock changes."""
        try:
            # Get monitor dimensions
            monitor = sct.monitors[monitor_id]
            width = monitor['width']
            height = monitor['height']
            
            # Define multiple sample areas (avoiding corners where clocks usually are)
            sample_size = 100  # 100x100 pixel samples
            sample_areas = [
                # Center
                {
                    'top': monitor['top'] + height // 2 - sample_size // 2,
                    'left': monitor['left'] + width // 2 - sample_size // 2,
                    'width': sample_size,
                    'height': sample_size
                },
                # Left middle
                {
                    'top': monitor['top'] + height // 2 - sample_size // 2,
                    'left': monitor['left'] + width // 4 - sample_size // 2,
                    'width': sample_size,
                    'height': sample_size
                },
                # Right middle
                {
                    'top': monitor['top'] + height // 2 - sample_size // 2,
                    'left': monitor['left'] + 3 * width // 4 - sample_size // 2,
                    'width': sample_size,
                    'height': sample_size
                }
            ]
            
            # Capture all sample areas and combine hashes
            combined_hash = hashlib.md5()
            for area in sample_areas:
                try:
                    screenshot = sct.grab(area)
                    screenshot_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)
                    combined_hash.update(screenshot_bytes)
                except:
                    # If any sample fails, skip it
                    continue
            
            return combined_hash.hexdigest()
            
        except Exception as e:
            print(f"Hash generation failed for monitor {monitor_id}: {e}")
            return None
    
    def update_idle_skip_counter(self):
        """Update the idle skip counter in the menu."""
        self.skip_counter_item.title = f"Idle Skips: {self.idle_skip_count}"
        print(f"[DEBUG] Updated idle skip counter to: {self.idle_skip_count}")

    def take_auto_screenshot(self, sender):
        """Take automatic screenshots without user interaction, with duplicate detection."""
        try:
            timestamp = datetime.now()
            date_folder = timestamp.strftime("%Y-%m-%d")
            time_filename_base = timestamp.strftime("%H-%M-%S")
            
            # Create directory for today's captures
            today_captures_dir = os.path.join(CAPTURES_DIR, date_folder)
            os.makedirs(today_captures_dir, exist_ok=True)
            
            # Check for changes before saving
            with mss.mss() as sct:
                current_hashes = {}
                has_changes = False
                
                # Get hashes for all monitors
                for i, monitor in enumerate(sct.monitors[1:], 1):
                    current_hash = self.get_screenshot_hash(sct, i)
                    current_hashes[i] = current_hash
                    
                    # Compare with previous hash
                    previous_hash = self.previous_screenshot_hashes.get(i)
                    if previous_hash is None or previous_hash != current_hash:
                        has_changes = True
                        print(f"[DEBUG] Monitor {i}: Changes detected (prev: {previous_hash[:8] if previous_hash else 'None'}..., curr: {current_hash[:8] if current_hash else 'None'}...)")
                    else:
                        print(f"[DEBUG] Monitor {i}: No changes (hash: {current_hash[:8] if current_hash else 'None'}...)")
                
                if has_changes:
                    # Save screenshots only if there are changes
                    screenshot_count = 0
                    for i, monitor in enumerate(sct.monitors[1:], 1):
                        filename = os.path.join(today_captures_dir, f"{time_filename_base}-auto-screen-{i}.png")
                        sct.shot(mon=i, output=filename)
                        screenshot_count += 1
                    
                    # Update previous hashes
                    self.previous_screenshot_hashes = current_hashes
                    
                    # Update menu bar title to show last capture time
                    self.title = f"📸 {timestamp.strftime('%H:%M')}"
                    print(f"[DEBUG] Screenshots saved - changes detected")
                else:
                    # No changes detected, increment skip counter
                    self.idle_skip_count += 1
                    self.update_idle_skip_counter()
                    
                    # Update title to show skip
                    self.title = f"📸 {timestamp.strftime('%H:%M')} (skip)"
                    print(f"[DEBUG] Screenshots skipped - no changes (skip count: {self.idle_skip_count})")
            
        except Exception as e:
            # Silent failure for auto-screenshots to avoid interrupting user
            print(f"Auto-screenshot failed: {e}")
    
    @rumps.clicked("Auto Screenshots: ON")
    def toggle_auto_screenshots(self, sender):
        """Toggle automatic screenshot functionality."""
        self.auto_screenshots_enabled = not self.auto_screenshots_enabled
        
        if self.auto_screenshots_enabled:
            self.auto_toggle_item.title = "Auto Screenshots: ON"
            # Reset counters when re-enabling
            self.idle_skip_count = 0
            self.previous_screenshot_hashes = {}
            self.update_idle_skip_counter()
            self.start_auto_screenshots()
            rumps.notification(
                title=APP_NAME,
                subtitle="Auto Screenshots Enabled",
                message=f"Taking screenshots every {SCREENSHOT_INTERVAL} seconds"
            )
        else:
            self.auto_toggle_item.title = "Auto Screenshots: OFF"
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