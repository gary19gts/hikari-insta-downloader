#!/usr/bin/env python3
"""
Hikari Insta Downloader - Smart Launcher
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

Checks dependencies and launches the application
"""

import sys
import os
import subprocess
import importlib

def check_dependency(package_name, import_name=None, install_command=None):
    """Check if a dependency is available"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        if install_command:
            print(f"❌ {package_name} not found")
            response = input(f"Install {package_name}? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", install_command])
                    print(f"✅ {package_name} installed successfully")
                    return True
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {package_name}")
                    return False
            else:
                return False
        return False

def main():
    print("🚀 Hikari Insta Downloader - Smart Launcher")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - OK")
    
    # Check required packages
    required_packages = [
        ("customtkinter", "customtkinter", "customtkinter>=5.2.0"),
        ("Pillow", "PIL", "Pillow>=10.0.0"),
        ("requests", "requests", "requests>=2.31.0")
    ]
    
    print("\n📦 Checking required packages...")
    all_deps_ok = True
    
    for package_name, import_name, install_cmd in required_packages:
        if not check_dependency(package_name, import_name, install_cmd):
            all_deps_ok = False
    
    if not all_deps_ok:
        print("\n❌ Some required packages are missing.")
        print("Please install them manually or run: python install.py")
        return False
    
    # Check download engines (optional but recommended)
    print("\n🔧 Checking download engines...")
    engines = ["yt-dlp", "instaloader", "gallery-dl"]
    available_engines = []
    
    for engine in engines:
        try:
            subprocess.run([engine, "--version"], 
                          capture_output=True, 
                          check=True, 
                          timeout=3)
            print(f"✅ {engine} - Available")
            available_engines.append(engine)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            print(f"⚠️  {engine} - Not available")
    
    if not available_engines:
        print("\n⚠️  No download engines found!")
        print("Install at least one: pip install yt-dlp instaloader gallery-dl")
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response not in ['y', 'yes']:
            return False
    
    # Create Downloads folder
    downloads_folder = os.path.join(os.getcwd(), "Downloads")
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder, exist_ok=True)
        print(f"✅ Created Downloads folder: {downloads_folder}")
    
    # Launch the application
    print("\n🎯 All checks passed! Launching Hikari Insta Downloader...")
    print("=" * 50)
    
    try:
        # Import and run the main application
        from main import HikariDownloader
        app = HikariDownloader()
        app.run()
        return True
    except ImportError as e:
        print(f"❌ Failed to import main application: {e}")
        print("Make sure main.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")