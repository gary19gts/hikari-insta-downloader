#!/usr/bin/env python3
"""
Hikari Insta Downloader - Main Application
Copyright (C) 2025 Gary19gts

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Version: 1.2
Date: October 2025
Made by: Gary19gts

A modern Instagram content downloader with Apple-style interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import threading
import os
import sys
import subprocess
import requests
from pathlib import Path
import json
import logging
from datetime import datetime
import re
import webbrowser
try:
    from PIL import Image, ImageTk
except ImportError:
    print("⚠️ PIL/Pillow not found. Icon functionality may be limited.")

# Configure CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class HikariDownloader:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Hikari Insta Downloader - Made by Gary19gts")
        self.root.geometry("1000x720")
        self.root.minsize(800, 600)
        
        # Set window icon
        self.set_window_icon()
        
        # Load configuration
        self.config = self.load_config()
        
        # Create Downloads folder if it doesn't exist
        downloads_folder = os.path.join(os.getcwd(), "Downloads")
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder, exist_ok=True)
        
        # Variables
        self.output_folder = tk.StringVar(value=downloads_folder)
        self.url_var = tk.StringVar()
        self.engine_var = tk.StringVar(value=self.config.get("default_settings", {}).get("default_engine", "instaloader"))
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        
        # Setup logging
        self.setup_logging()
        
        # Initialize UI
        self.setup_ui()
        
        # Bind URL change event
        self.url_var.trace('w', self.on_url_change)
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def set_window_icon(self):
        """Set window icon with multiple fallback methods"""
        icon_files = ["hikari_icon.ico", "favicon.ico", "icon.ico", "hikari_icon_32x32.png", "icon_32x32.png", "hikari_icon.png", "icon.png"]
        
        for icon_file in icon_files:
            if os.path.exists(icon_file):
                try:
                    # Method 1: Direct iconbitmap (works with .ico files)
                    if icon_file.endswith('.ico'):
                        self.root.iconbitmap(icon_file)
                        print(f"✅ Icon set successfully: {icon_file}")
                        return
                    
                    # Method 2: Using PhotoImage for PNG files
                    elif icon_file.endswith('.png'):
                        from PIL import Image, ImageTk
                        img = Image.open(icon_file)
                        img = img.resize((32, 32), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.root.iconphoto(True, photo)
                        # Keep a reference to prevent garbage collection
                        self.root._icon_photo = photo
                        print(f"✅ Icon set successfully: {icon_file}")
                        return
                        
                except Exception as e:
                    print(f"⚠️ Could not set icon {icon_file}: {e}")
                    continue
        
        print("⚠️ No suitable icon file found or all methods failed")
    
    def setup_logging(self):
        """Setup logging for diagnostics"""
        log_level = self.config.get("default_settings", {}).get("log_level", "INFO")
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('hikari_downloader.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Set white background for root window
        self.root.configure(fg_color="white")
        
        # Main container with white background
        main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create two columns with white background
        left_column = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="white", border_width=1, border_color="#E5E5E5")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_column = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="white", border_width=1, border_color="#E5E5E5")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.setup_left_column(left_column)
        self.setup_right_column(right_column)
        
    def setup_left_column(self, parent):
        """Setup left column with controls"""
        # Title
        title_label = ctk.CTkLabel(
            parent, 
            text="📷 Hikari Insta Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Disclaimer
        disclaimer_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color=("#FFE6E6", "#4A1A1A"))
        disclaimer_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        disclaimer_text = ctk.CTkLabel(
            disclaimer_frame,
            text="⚠️ DISCLAIMER: Only download your own content or content you have permission to download.",
            font=ctk.CTkFont(size=12),
            text_color=("#CC0000", "#FF6666"),
            wraplength=300
        )
        disclaimer_text.pack(pady=15, padx=15)
        
        # URL Input
        url_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white", border_width=1, border_color="#E5E5E5")
        url_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        url_label = ctk.CTkLabel(url_frame, text="Instagram URL:", font=ctk.CTkFont(size=14, weight="bold"))
        url_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            textvariable=self.url_var,
            placeholder_text="Paste Instagram URL here...",
            height=40,
            corner_radius=8
        )
        self.url_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Content Detection Strip (new)
        self.detection_strip = ctk.CTkFrame(parent, corner_radius=8, fg_color=("#F5F5F5", "#2B2B2B"), border_width=1, border_color=("#CCCCCC", "#555555"))
        self.detection_strip.pack(fill="x", padx=20, pady=(0, 15))
        
        self.detection_label = ctk.CTkLabel(
            self.detection_strip,
            text="⏳ Waiting for URL...",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#666666", "#AAAAAA")
        )
        self.detection_label.pack(pady=12)
        
        # Engine Selection
        engine_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white", border_width=1, border_color="#E5E5E5")
        engine_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        engine_title_frame = ctk.CTkFrame(engine_frame, fg_color="transparent")
        engine_title_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        engine_label = ctk.CTkLabel(engine_title_frame, text="Download Engine:", font=ctk.CTkFont(size=14, weight="bold"))
        engine_label.pack(side="left")
        
        info_button = ctk.CTkButton(
            engine_title_frame,
            text="i",
            width=25,
            height=25,
            corner_radius=12,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.show_engine_info
        )
        info_button.pack(side="right")
        
        self.engine_combo = ctk.CTkComboBox(
            engine_frame,
            values=["instaloader", "yt-dlp", "gallery-dl"],
            variable=self.engine_var,
            height=35,
            corner_radius=8
        )
        self.engine_combo.pack(fill="x", padx=15, pady=(0, 10))
        
        # Engine guidance
        guidance_frame = ctk.CTkFrame(engine_frame, corner_radius=8, fg_color=("#F0F8FF", "#1E3A5F"))
        guidance_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        guidance_text = ctk.CTkLabel(
            guidance_frame,
            text="💡 Quick Guide:\n📸 Instaloader: Best for photos and image posts\n🎥 yt-dlp: Best for videos and reels",
            font=ctk.CTkFont(size=11),
            text_color=("#0066CC", "#4A9EFF"),
            justify="left"
        )
        guidance_text.pack(pady=10, padx=15)
        
        # Output Folder
        folder_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white", border_width=1, border_color="#E5E5E5")
        folder_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        folder_label = ctk.CTkLabel(folder_frame, text="Output Folder:", font=ctk.CTkFont(size=14, weight="bold"))
        folder_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        folder_controls = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_controls.pack(fill="x", padx=15, pady=(0, 15))
        
        self.folder_entry = ctk.CTkEntry(
            folder_controls,
            textvariable=self.output_folder,
            height=35,
            corner_radius=8
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(
            folder_controls,
            text="Browse",
            width=80,
            height=35,
            corner_radius=8,
            command=self.browse_folder
        )
        browse_button.pack(side="right", padx=(0, 5))
        
        open_button = ctk.CTkButton(
            folder_controls,
            text="Open",
            width=60,
            height=35,
            corner_radius=8,
            command=self.open_folder
        )
        open_button.pack(side="right", padx=(0, 5))
        
        # Download Button
        self.download_button = ctk.CTkButton(
            parent,
            text="Download Content",
            height=50,
            corner_radius=12,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#E4405F", "#C13584"),
            hover_color=("#C13584", "#A02D72"),
            command=self.start_download
        )
        self.download_button.pack(fill="x", padx=20, pady=(0, 15))
        
        # Progress Bar
        progress_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white", border_width=1, border_color="#E5E5E5")
        progress_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, corner_radius=8)
        self.progress_bar.pack(fill="x", padx=15, pady=15)
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            progress_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(0, 15))
        

        
    def setup_right_column(self, parent):
        """Setup right column for support and info"""
        # Support Development section (larger and more prominent)
        support_frame = ctk.CTkFrame(parent, corner_radius=15, fg_color="white", border_width=1, border_color="#E5E5E5")
        support_frame.pack(fill="both", expand=True, padx=20, pady=(20, 15))
        
        support_title = ctk.CTkLabel(
            support_frame,
            text="☕ Support Development",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#333333", "#CCCCCC")
        )
        support_title.pack(pady=(20, 10))
        
        support_text = ctk.CTkLabel(
            support_frame,
            text="If you find Hikari useful, consider supporting its development!",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=280
        )
        support_text.pack(pady=(0, 15))
        
        kofi_button = ctk.CTkButton(
            support_frame,
            text="☕ Buy me a coffee on Ko-fi",
            height=45,
            corner_radius=10,
            fg_color=("#FF5E5B", "#FF7875"),
            hover_color=("#FF4444", "#FF6666"),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            command=self.open_kofi
        )
        kofi_button.pack(fill="x", padx=15, pady=(0, 15))
        
        thanks_label = ctk.CTkLabel(
            support_frame,
            text="Thank you for your support! 🖤",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        thanks_label.pack(pady=(0, 20))
        
        # Diagnostic Button (moved from left column)
        diagnostic_button = ctk.CTkButton(
            parent,
            text="Run Diagnostics",
            height=40,
            corner_radius=10,
            fg_color=("#34C759", "#30D158"),
            hover_color=("#28A745", "#28A745"),
            command=self.run_diagnostics
        )
        diagnostic_button.pack(fill="x", padx=20, pady=(0, 15))
        
        # App info section at bottom
        info_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        info_text = f"""
{self.config.get('app_info', {}).get('name', 'Hikari Insta Downloader')}
Version: {self.config.get('app_info', {}).get('version', '1.0.0')}
{self.config.get('app_info', {}).get('date', 'October 2025')}
Made by: {self.config.get('app_info', {}).get('author', 'Gary19gts')}
        """.strip()
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color="gray",
            justify="center"
        )
        info_label.pack(pady=10)
        
        # Bottom buttons frame (centered alignment)
        bottom_buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        bottom_buttons_frame.pack(padx=20, pady=(0, 20))
        
        # Credits button
        credits_button = ctk.CTkButton(
            bottom_buttons_frame,
            text="Credits & Thanks",
            width=120,
            height=35,
            corner_radius=8,
            command=self.show_credits
        )
        credits_button.pack(side="left", padx=(0, 10))
        
        # Update button (same color as credits button)
        update_button = ctk.CTkButton(
            bottom_buttons_frame,
            text="Update Libraries",
            width=120,
            height=35,
            corner_radius=8,
            command=self.update_libraries
        )
        update_button.pack(side="left")
        
    def on_url_change(self, *args):
        """Handle URL input changes"""
        url = self.url_var.get().strip()
        if url and self.is_valid_instagram_url(url):
            self.update_preview(url)
        else:
            self.clear_preview()
    
    def is_valid_instagram_url(self, url):
        """Check if URL is a valid Instagram URL"""
        instagram_patterns = [
            r'https?://(?:www\.)?instagram\.com/p/[^/]+/?',
            r'https?://(?:www\.)?instagram\.com/reel/[^/]+/?',
            r'https?://(?:www\.)?instagram\.com/stories/[^/]+/[^/]+/?'
        ]
        return any(re.match(pattern, url) for pattern in instagram_patterns)
    
    def update_preview(self, url):
        """Update detection strip with URL information"""
        # Analyze URL
        url_info = self.analyze_url(url)
        
        # Determine icon and message based on content type
        if url_info['content'] == 'video' or 'Reel' in url_info['type']:
            icon = "🎥"
            content_type = "Video Content"
        else:
            icon = "📸"
            content_type = "Image Content"
        
        # Update detection strip with green styling
        self.detection_label.configure(
            text=f"✅ {url_info['type']} detected - {content_type} ready to download",
            text_color=("#34C759", "#30D158")
        )
        
        # Update strip colors to green
        self.detection_strip.configure(
            fg_color=("#E8F5E8", "#1A4A1A"),
            border_color=("#34C759", "#30D158")
        )
    
    def clear_preview(self):
        """Clear detection strip"""
        self.detection_label.configure(
            text="⏳ Waiting for URL...",
            text_color=("#666666", "#AAAAAA")
        )
        
        # Reset strip colors to gray
        self.detection_strip.configure(
            fg_color=("#F5F5F5", "#2B2B2B"),
            border_color=("#CCCCCC", "#555555")
        )
    
    def analyze_url(self, url):
        """Analyze Instagram URL to determine content type"""
        if '/p/' in url:
            return {'type': 'Instagram Post', 'content': 'photo/video'}
        elif '/reel/' in url:
            return {'type': 'Instagram Reel', 'content': 'video'}
        elif '/stories/' in url:
            return {'type': 'Instagram Story', 'content': 'photo/video'}
        else:
            return {'type': 'Instagram Content', 'content': 'unknown'}
    
    def open_kofi(self):
        """Open Ko-fi support page"""
        try:
            webbrowser.open("https://ko-fi.com/gary19gts")
        except Exception as e:
            self.logger.error(f"Failed to open Ko-fi link: {str(e)}")
            messagebox.showinfo("Ko-fi Link", "Visit: https://ko-fi.com/gary19gts\n\nThank you for your support!")
    
    def update_libraries(self):
        """Update all libraries automatically"""
        update_window = ctk.CTkToplevel(self.root)
        update_window.title("Update Libraries")
        update_window.geometry("500x400")
        update_window.transient(self.root)
        update_window.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(update_window, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🔄 Update Libraries",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#007AFF", "#0A84FF")
        )
        title_label.pack(pady=(20, 15))
        
        # Progress text area
        progress_text = ctk.CTkTextbox(main_frame, corner_radius=10, font=ctk.CTkFont(size=11))
        progress_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Progress bar
        progress_bar = ctk.CTkProgressBar(main_frame, corner_radius=8)
        progress_bar.pack(fill="x", padx=20, pady=(0, 15))
        progress_bar.set(0)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Start update button
        start_button = ctk.CTkButton(
            buttons_frame,
            text="Start Update",
            height=40,
            corner_radius=10,
            fg_color=("#34C759", "#30D158"),
            hover_color=("#28A745", "#28A745"),
            command=lambda: self.start_update_process(progress_text, progress_bar, start_button, close_button)
        )
        start_button.pack(side="left", padx=(0, 10))
        
        # Close button
        close_button = ctk.CTkButton(
            buttons_frame,
            text="Close",
            height=40,
            corner_radius=10,
            command=update_window.destroy
        )
        close_button.pack(side="right")
        
        # Initial message
        initial_message = """📦 Library Update Manager

This will update the following libraries to their latest versions:
• customtkinter
• requests
• yt-dlp
• instaloader
• gallery-dl
• pillow

⚠️ Note: This process may take a few minutes depending on your internet connection.

Click 'Start Update' to begin the process.
"""
        progress_text.insert("1.0", initial_message)
        progress_text.configure(state="disabled")
    
    def start_update_process(self, progress_text, progress_bar, start_button, close_button):
        """Start the library update process in a separate thread"""
        start_button.configure(state="disabled", text="Updating...")
        close_button.configure(state="disabled")
        
        # Start update in separate thread
        threading.Thread(
            target=self.update_libraries_thread,
            args=(progress_text, progress_bar, start_button, close_button),
            daemon=True
        ).start()
    
    def update_libraries_thread(self, progress_text, progress_bar, start_button, close_button):
        """Update libraries in a separate thread"""
        libraries = [
            "customtkinter>=5.2.0",
            "requests>=2.31.0", 
            "yt-dlp",
            "instaloader",
            "gallery-dl",
            "pillow>=10.0.0"
        ]
        
        total_libs = len(libraries)
        
        def update_progress_text(message):
            progress_text.configure(state="normal")
            progress_text.insert("end", f"\n{message}")
            progress_text.see("end")
            progress_text.configure(state="disabled")
            progress_text.update()
        
        try:
            update_progress_text("🚀 Starting library updates...")
            
            for i, library in enumerate(libraries):
                update_progress_text(f"📦 Updating {library}...")
                progress_bar.set((i + 0.5) / total_libs)
                
                try:
                    # Run pip install --upgrade
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "--upgrade", library],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    
                    if result.returncode == 0:
                        update_progress_text(f"✅ {library} updated successfully")
                    else:
                        update_progress_text(f"⚠️ {library} update had issues: {result.stderr[:100]}")
                        
                except subprocess.TimeoutExpired:
                    update_progress_text(f"⏰ {library} update timed out")
                except Exception as e:
                    update_progress_text(f"❌ {library} update failed: {str(e)[:100]}")
                
                progress_bar.set((i + 1) / total_libs)
            
            update_progress_text("\n🎉 Library update process completed!")
            update_progress_text("💡 Restart the application to use the updated libraries.")
            
        except Exception as e:
            update_progress_text(f"\n❌ Update process failed: {str(e)}")
        
        finally:
            # Re-enable buttons
            start_button.configure(state="normal", text="Update Complete")
            close_button.configure(state="normal")

    
    def show_credits(self):
        """Show credits and acknowledgments window"""
        credits_window = ctk.CTkToplevel(self.root)
        credits_window.title("Credits & Thanks")
        credits_window.geometry("600x500")
        credits_window.transient(self.root)
        credits_window.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(credits_window, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="❤️ Credits & Thanks",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#E4405F", "#C13584")
        )
        title_label.pack(pady=(20, 15))
        
        # Scrollable text area
        text_widget = ctk.CTkTextbox(main_frame, corner_radius=10, font=ctk.CTkFont(size=12))
        text_widget.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        credits_text = """🎉 HIKARI INSTA DOWNLOADER v1.2

👨‍💻 DEVELOPED BY:
Gary19gts - Main Developer & UI Designer
October 2025

🙏 SPECIAL THANKS TO THE AMAZING LIBRARY CREATORS:

📦 DOWNLOAD ENGINES:
• yt-dlp Team - The most powerful media downloader
  → Reliable, fast, and constantly updated
  → GitHub: https://github.com/yt-dlp/yt-dlp

• instaloader Team - Instagram specialized downloader  
  → Perfect for Instagram content
  → GitHub: https://github.com/instaloader/instaloader

• gallery-dl Team - Multi-platform media downloader
  → Supports numerous platforms
  → GitHub: https://github.com/mikf/gallery-dl

🎨 USER INTERFACE:
• CustomTkinter by Tom Schimansky
  → Modern and beautiful GUI framework
  → GitHub: https://github.com/TomSchimansky/CustomTkinter

• Tkinter - Python's standard GUI library
  → Foundation of the interface

🖼️ IMAGE PROCESSING:
• Pillow (PIL) Team
  → Image processing and thumbnail generation
  → GitHub: https://github.com/python-pillow/Pillow

🌐 NETWORKING:
• Requests Library by Kenneth Reitz
  → HTTP requests made simple
  → GitHub: https://github.com/psf/requests

🐍 PYTHON COMMUNITY:
• Python Software Foundation
  → The amazing Python programming language
  → Making development accessible and fun

💝 INSPIRATION:
• Apple Inc. - For the clean design inspiration
• Instagram - For creating an amazing platform
• Open Source Community - For making this possible

⚖️ LEGAL NOTICE:
This application is for educational purposes and personal use only.
Always respect copyright laws and platform terms of service.
Only download content you own or have permission to download.

🌟 THANK YOU:
To everyone who uses, tests, and provides feedback on this application.
Your support makes development worthwhile!

Made with ❤️ and lots of ☕
"""
        
        text_widget.insert("1.0", credits_text)
        text_widget.configure(state="disabled")
        
        # Close button
        close_button = ctk.CTkButton(
            main_frame,
            text="Close",
            height=40,
            corner_radius=10,
            fg_color=("#E4405F", "#C13584"),
            hover_color=("#C13584", "#A02D72"),
            command=credits_window.destroy
        )
        close_button.pack(pady=(0, 20))
    
    def show_engine_info(self):
        """Show information about download engines"""
        engines_config = self.config.get("engines", {})
        
        info_text = "Download Engines Information:\n\n"
        
        for engine_key, engine_info in engines_config.items():
            name = engine_info.get("name", engine_key)
            desc = engine_info.get("description", "")
            advantages = engine_info.get("advantages", [])
            recommended = engine_info.get("recommended", False)
            
            info_text += f"🔹 {name}"
            if recommended:
                info_text += " (Recommended)"
            info_text += f"\n• {desc}\n"
            
            for advantage in advantages:
                info_text += f"• {advantage}\n"
            info_text += "\n"
        
        info_text += "💡 Tips:\n📸 Use instaloader for photos and image posts\n🎥 Use yt-dlp for videos and reels\n🌐 Use gallery-dl for multi-platform downloads"
        
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Engine Information")
        info_window.geometry("500x450")
        info_window.transient(self.root)
        info_window.grab_set()
        
        text_widget = ctk.CTkTextbox(info_window, corner_radius=10)
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")
        
    def browse_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(initialdir=self.output_folder.get())
        if folder:
            self.output_folder.set(folder)
            
    def open_folder(self):
        """Open output folder in file explorer"""
        folder = self.output_folder.get()
        if os.path.exists(folder):
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.run(["open", folder])
            else:
                subprocess.run(["xdg-open", folder])
        else:
            messagebox.showerror("Error", "Folder does not exist!")
            
    def start_download(self):
        """Start the download process"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter an Instagram URL!")
            return
            
        if not self.is_valid_instagram_url(url):
            messagebox.showerror("Error", "Please enter a valid Instagram URL!\n\nSupported formats:\n• Posts: instagram.com/p/...\n• Reels: instagram.com/reel/...\n• Stories: instagram.com/stories/...")
            return
        
        # Check if output folder exists
        output_dir = self.output_folder.get()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create output folder: {str(e)}")
                return
        
        # Check if output folder is writable
        if not os.access(output_dir, os.W_OK):
            messagebox.showerror("Error", "Output folder is not writable! Please choose a different folder.")
            return
            
        # Start download in separate thread
        self.download_button.configure(state="disabled", text="Downloading...")
        self.progress_bar.set(0)
        threading.Thread(target=self.download_content, daemon=True).start()
        
    def download_content(self):
        """Download content using selected engine"""
        try:
            url = self.url_var.get().strip()
            engine = self.engine_var.get()
            output_dir = self.output_folder.get()
            
            self.status_var.set("Preparing download...")
            self.progress_bar.set(0.1)
            
            if engine == "yt-dlp":
                self.download_with_ytdlp(url, output_dir)
            elif engine == "instaloader":
                self.download_with_instaloader(url, output_dir)
            elif engine == "gallery-dl":
                self.download_with_gallerydl(url, output_dir)
                
            self.status_var.set("Download completed successfully!")
            self.progress_bar.set(1.0)
            messagebox.showinfo("Success", "Download completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Download failed: {str(e)}")
            self.status_var.set("Download failed!")
            messagebox.showerror("Error", f"Download failed: {str(e)}")
        finally:
            self.download_button.configure(state="normal", text="Download Content")
            
    def download_with_ytdlp(self, url, output_dir):
        """Download using yt-dlp"""
        self.status_var.set("Preparing yt-dlp download...")
        self.progress_bar.set(0.2)
        
        # Check if yt-dlp is available
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("yt-dlp is not installed. Please run: pip install yt-dlp")
        
        cmd = [
            "yt-dlp",
            "--output", f"{output_dir}/%(uploader)s_%(title)s.%(ext)s",
            "--write-info-json",
            "--write-thumbnail",
            "--no-warnings",
            url
        ]
        
        self.status_var.set("Downloading with yt-dlp...")
        self.progress_bar.set(0.6)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error occurred"
            raise Exception(f"yt-dlp failed: {error_msg}")
        
        self.progress_bar.set(0.9)
            
    def download_with_instaloader(self, url, output_dir):
        """Download using instaloader"""
        self.status_var.set("Preparing instaloader download...")
        self.progress_bar.set(0.2)
        
        # Check if instaloader is available
        try:
            subprocess.run(["instaloader", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("instaloader is not installed. Please run: pip install instaloader")
        
        # Extract shortcode from URL
        shortcode_match = re.search(r'/(?:p|reel)/([^/]+)/', url)
        if not shortcode_match:
            raise Exception("Could not extract content ID from URL")
            
        shortcode = shortcode_match.group(1)
        
        cmd = [
            "instaloader",
            "--dirname-pattern", output_dir,
            "--no-metadata-json",
            "--", f"-{shortcode}"
        ]
        
        self.status_var.set("Downloading with instaloader...")
        self.progress_bar.set(0.6)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error occurred"
            raise Exception(f"instaloader failed: {error_msg}")
        
        self.progress_bar.set(0.9)
            
    def download_with_gallerydl(self, url, output_dir):
        """Download using gallery-dl"""
        self.status_var.set("Preparing gallery-dl download...")
        self.progress_bar.set(0.2)
        
        # Check if gallery-dl is available
        try:
            subprocess.run(["gallery-dl", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("gallery-dl is not installed. Please run: pip install gallery-dl")
        
        cmd = [
            "gallery-dl",
            "--destination", output_dir,
            "--quiet",
            url
        ]
        
        self.status_var.set("Downloading with gallery-dl...")
        self.progress_bar.set(0.6)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error occurred"
            raise Exception(f"gallery-dl failed: {error_msg}")
        
        self.progress_bar.set(0.9)
            
    def run_diagnostics(self):
        """Run system diagnostics"""
        diagnostic_window = ctk.CTkToplevel(self.root)
        diagnostic_window.title("System Diagnostics")
        diagnostic_window.geometry("600x500")
        diagnostic_window.transient(self.root)
        diagnostic_window.grab_set()
        
        text_widget = ctk.CTkTextbox(diagnostic_window, corner_radius=10)
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Run diagnostics
        diagnostics = self.get_diagnostics()
        text_widget.insert("1.0", diagnostics)
        text_widget.configure(state="disabled")
        
    def get_diagnostics(self):
        """Get system diagnostics information"""
        diagnostics = []
        diagnostics.append("=== HIKARI DOWNLOADER DIAGNOSTICS ===\n")
        diagnostics.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Python version
        diagnostics.append(f"Python Version: {sys.version}\n")
        
        # Check dependencies
        dependencies = ["yt-dlp", "instaloader", "gallery-dl", "requests", "pillow"]
        diagnostics.append("=== DEPENDENCY CHECK ===\n")
        
        for dep in dependencies:
            try:
                result = subprocess.run([dep, "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    diagnostics.append(f"✅ {dep}: Available\n")
                else:
                    diagnostics.append(f"❌ {dep}: Not working properly\n")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                diagnostics.append(f"❌ {dep}: Not installed\n")
        
        # Output folder check
        diagnostics.append(f"\n=== OUTPUT FOLDER ===\n")
        output_dir = self.output_folder.get()
        if os.path.exists(output_dir):
            diagnostics.append(f"✅ Output folder exists: {output_dir}\n")
            if os.access(output_dir, os.W_OK):
                diagnostics.append("✅ Output folder is writable\n")
            else:
                diagnostics.append("❌ Output folder is not writable\n")
        else:
            diagnostics.append(f"❌ Output folder does not exist: {output_dir}\n")
        
        # Network check
        diagnostics.append("\n=== NETWORK CHECK ===\n")
        try:
            response = requests.get("https://www.instagram.com", timeout=5)
            if response.status_code == 200:
                diagnostics.append("✅ Instagram is accessible\n")
            else:
                diagnostics.append(f"⚠️ Instagram returned status code: {response.status_code}\n")
        except Exception as e:
            diagnostics.append(f"❌ Cannot reach Instagram: {str(e)}\n")
        
        return "".join(diagnostics)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = HikariDownloader()
    app.run()