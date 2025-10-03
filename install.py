#!/usr/bin/env python3
"""
Hikari Insta Downloader - Installation Script
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

Automatically installs all required dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("🚀 Hikari Insta Downloader - Installation Script")
    print("=" * 50)
    
    # Required packages
    packages = [
        "customtkinter>=5.2.0",
        "requests>=2.31.0",
        "yt-dlp",
        "instaloader",
        "gallery-dl"
    ]
    
    print("Installing required packages...")
    
    failed_packages = []
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    
    if not failed_packages:
        print("🎉 All packages installed successfully!")
        print("\nYou can now run the application with:")
        print("python main.py")
    else:
        print("⚠️  Some packages failed to install:")
        for package in failed_packages:
            print(f"   - {package}")
        print("\nPlease install them manually using:")
        print("pip install <package_name>")
    
    print("\n📝 Note: Make sure you have Python 3.7+ installed")
    print("🔧 For video processing, consider installing FFmpeg separately")

if __name__ == "__main__":
    main()