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
APP_ICON = "📸"
SCREENSHOT_INTERVAL = 60  # seconds 

class MacCappyApp(rumps.App):
    def __init__(self):
        super(MacCappyApp, self).__init__(APP_NAME, icon=None, title=APP_ICON)
        
        # Initialize skip counter and previous screenshot hashes
        self.idle_skip_count = 0
        self.manual_capture_count = 0
        self.previous_screenshot_hashes = {}  # monitor_id -> hash
        
        # Create menu items with references
        self.auto_toggle_item = rumps.MenuItem("Auto Screenshots: ON", callback=self.toggle_auto_screenshots)
        self.skip_counter_item = rumps.MenuItem("Idle Skips: 0", callback=None)
        self.manual_counter_item = rumps.MenuItem("Manual Captures: 0", callback=None)
        
        self.menu = [
            "Manual Capture", 
            "---", 
            self.auto_toggle_item,
            self.skip_counter_item,
            self.manual_counter_item,
            "---",
            "Debug: Open Today's Captures", 
            "---"
        ]
        
        # Ensure base directories exist
        try:
            os.makedirs(CAPTURES_DIR, exist_ok=True)
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
        Excludes top 10% of screen to avoid clock changes."""
        try:
            # Get monitor dimensions
            monitor = sct.monitors[monitor_id]
            width = monitor['width']
            height = monitor['height']
            
            # Define area excluding top 10% (where clock/menu bar usually are)
            exclude_top_percent = 0.10
            top_margin = int(height * exclude_top_percent)
            
            capture_area = {
                'top': monitor['top'] + top_margin,
                'left': monitor['left'],
                'width': width,
                'height': height - top_margin
            }
            
            # Capture the screen area excluding the top
            screenshot = sct.grab(capture_area)
            
            # Convert to bytes and hash
            screenshot_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)
            return hashlib.md5(screenshot_bytes).hexdigest()
            
        except Exception as e:
            print(f"Hash generation failed for monitor {monitor_id}: {e}")
            return None
    
    def update_idle_skip_counter(self):
        """Update the idle skip counter in the menu."""
        self.skip_counter_item.title = f"Idle Skips: {self.idle_skip_count}"
        print(f"[DEBUG] Updated idle skip counter to: {self.idle_skip_count}")
    
    def update_manual_capture_counter(self):
        """Update the manual capture counter in the menu."""
        self.manual_counter_item.title = f"Manual Captures: {self.manual_capture_count}"
        print(f"[DEBUG] Updated manual capture counter to: {self.manual_capture_count}")

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

    @rumps.clicked("Manual Capture")
    def capture_milestone(self, _):
        """Takes screenshots manually without note prompt."""
        timestamp = datetime.now()
        date_folder = timestamp.strftime("%Y-%m-%d")
        time_filename_base = timestamp.strftime("%H-%M-%S")
        
        # Create directory for today's captures
        today_captures_dir = os.path.join(CAPTURES_DIR, date_folder)
        
        try:
            os.makedirs(today_captures_dir, exist_ok=True)
        except Exception as e:
            rumps.alert(title="Directory Error", message=f"Failed to create today's folders: {e}")
            return
        
        # Capture screenshots of all monitors
        screenshot_paths = []
        try:
            with mss.mss() as sct:
                for i, monitor in enumerate(sct.monitors[1:], 1): # sct.monitors[0] is all screens
                    filename = os.path.join(today_captures_dir, f"{time_filename_base}-manual-screen-{i}.png")
                    sct.shot(mon=i, output=filename)
                    screenshot_paths.append(filename)
            
            # Increment manual capture counter
            self.manual_capture_count += 1
            self.update_manual_capture_counter()
                    
            rumps.notification(
                title=APP_NAME,
                subtitle="Manual Capture Complete!",
                message=f"Saved {len(screenshot_paths)} screen(s). Total manual captures: {self.manual_capture_count}"
            )
        except Exception as e:
            rumps.alert(title="Screenshot Error", message=f"Failed to capture screens: {e}")
            return

    @rumps.clicked("Debug: Open Today's Captures")
    def open_log_folder(self, _):
        """Opens today's captures directory in Finder."""
        timestamp = datetime.now()
        date_folder = timestamp.strftime("%Y-%m-%d")
        today_captures_dir = os.path.join(CAPTURES_DIR, date_folder)
        
        try:
            if os.path.exists(today_captures_dir):
                subprocess.run(["open", today_captures_dir])
                rumps.notification(
                    title=APP_NAME,
                    subtitle="Folder Opened",
                    message=f"Opened today's captures folder ({date_folder})"
                )
            else:
                # Create the directory first, then open it
                os.makedirs(today_captures_dir, exist_ok=True)
                subprocess.run(["open", today_captures_dir])
                rumps.notification(
                    title=APP_NAME,
                    subtitle="Folder Created & Opened",
                    message=f"Created and opened today's captures folder ({date_folder})"
                )
        except Exception as e:
            rumps.alert(title="Folder Error", message=f"Failed to open captures folder: {e}")

    def quit_application(self):
        """Clean shutdown of the application."""
        self.stop_auto_screenshots()
        rumps.quit_application()

if __name__ == "__main__":
    MacCappyApp().run()