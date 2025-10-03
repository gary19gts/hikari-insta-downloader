# 📷 Hikari Insta Downloader

<!--
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
-->

A modern Instagram content downloader with a clean Apple-style interface.

**Version:** 1.2  
**Date:** October 2025  
**Made by:** Gary19gts

## ⚠️ Important Disclaimer

**This application is intended for downloading your own content or content you have explicit permission to download. Please respect copyright laws and Instagram's Terms of Service.**

## Features

- 🎨 Modern Apple-style interface with clean white design
- 📱 Responsive layout that scales beautifully
- 🔧 Multiple download engines (instaloader, yt-dlp, gallery-dl)
- 🖼️ **Real-time thumbnail preview** of Instagram content
- 📁 Customizable output folder with quick access (default: Downloads/)
- 📊 Real-time download progress tracking
- 🔍 Built-in diagnostics system
- 💡 Helpful tooltips and engine selection guidance
- ❤️ **Credits & Thanks** button acknowledging all contributors
- 🌙 Clean light theme optimized for usability

## Supported Content

- Instagram posts (photos and videos)
- Instagram Reels
- Instagram Stories (if accessible)
- Multiple media in single posts

## Installation

### Option 1: Automatic Installation
```bash
python install.py
```

### Option 2: Manual Installation
```bash
pip install -r requirements.txt
pip install yt-dlp instaloader gallery-dl
```

### Requirements
- Python 3.7 or higher
- Internet connection
- Windows/macOS/Linux

## Usage

1. **Launch the application:**
   ```bash
   python main.py
   ```

2. **Enter Instagram URL:**
   - Paste any Instagram post, reel, or story URL
   - The URL should start with `https://www.instagram.com/`

3. **Select Download Engine:**
   - **yt-dlp** (Recommended): Most reliable, frequently updated
   - **instaloader**: Instagram-specialized, good for bulk downloads
   - **gallery-dl**: Multi-platform support

4. **Choose Output Folder:**
   - Default: Current directory
   - Click "Browse" to select custom folder
   - Click "Open" to view downloaded files

5. **Download:**
   - Click "Download Content" to start
   - Monitor progress in real-time
   - Files will be saved to your chosen folder

## Download Engines Comparison

| Engine | Reliability | Speed | Features | Best For |
|--------|-------------|-------|----------|----------|
| **instaloader** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Photos & Images (Default) |
| **yt-dlp** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Videos & Reels |
| **gallery-dl** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Multi-platform |

### 💡 Engine Selection Guide
- **📸 For Photos & Image Posts**: Use **instaloader** (default)
- **🎥 For Videos & Reels**: Use **yt-dlp**
- **🌐 For Multi-platform**: Use **gallery-dl**

## Troubleshooting

### Common Issues

1. **"Engine not found" error:**
   - Run the installation script again
   - Manually install: `pip install yt-dlp instaloader gallery-dl`

2. **Download fails:**
   - Check your internet connection
   - Verify the Instagram URL is correct and accessible
   - Try a different download engine
   - Run diagnostics for detailed information

3. **Permission errors:**
   - Ensure you have write permissions to the output folder
   - Try selecting a different output directory

### Diagnostics

Click the "Run Diagnostics" button to check:
- Python version and dependencies
- Download engine availability
- Output folder permissions
- Network connectivity to Instagram

## Interface Guide

### Left Column (Controls)
- **URL Input**: Paste Instagram links here
- **Engine Selection**: Choose your preferred download method with guidance
- **Output Folder**: Set where files will be saved (default: Downloads/)
- **Download Button**: Start the download process
- **Progress Bar**: Shows download status
- **Diagnostics**: System health check

### Right Column (Preview)
- **Content Preview**: Real-time thumbnail preview of Instagram content
- **Media Information**: Automatic content type detection
- **Credits Button**: Acknowledge all library creators and contributors
- **App Information**: Version and developer details

## File Structure

```
hikari-insta-downloader/
├── main.py              # Main application
├── install.py           # Installation script
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── hikari_downloader.log # Application logs
```

## Technical Details

- **GUI Framework**: CustomTkinter (modern tkinter)
- **Image Processing**: Pillow (PIL)
- **HTTP Requests**: requests library
- **Download Engines**: yt-dlp, instaloader, gallery-dl
- **Logging**: Built-in Python logging

## Legal Notice

This tool is for educational and personal use only. Users are responsible for:
- Complying with Instagram's Terms of Service
- Respecting copyright and intellectual property rights
- Only downloading content they own or have permission to download

## License

**Hikari Insta Downloader** is free software licensed under the **GNU Affero General Public License v3.0**.

- **Copyright (C) 2025 Gary19gts**
- **License**: AGPL-3.0
- **Full License Text**: See [LICENSE](LICENSE) file
- **License URL**: https://www.gnu.org/licenses/agpl-3.0.html

### What this means:
- ✅ You can use, modify, and distribute this software freely
- ✅ You can use it for commercial purposes
- ⚠️ If you distribute modified versions, you must also provide the source code
- ⚠️ If you run a modified version on a server, you must provide the source code to users
- ⚠️ Any derivative work must also be licensed under AGPL-3.0

For more details, see the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html).

## Support

If you encounter issues:
1. Run the built-in diagnostics
2. Check the log file (`hikari_downloader.log`)
3. Ensure all dependencies are properly installed
4. Verify your internet connection and Instagram URL

## Version History

- **v1.2** (October 2025): Stable release with modern GUI
  - Apple-style interface design
  - Multiple download engine support
  - Built-in diagnostics system
  - Real-time progress tracking

---

**Made with ❤️ by Gary19gts**

Thank you for using **Hikari Insta Downloader**!  
Made with ❤️ by Gary19gts  

If Hikari has been helpful to you, please consider supporting its development:  
☕ Buy me a coffee on Ko-fi → [https://ko-fi.com/gary19gts](https://ko-fi.com/gary19gts)  

✨ Even the smallest donation can bring a big light during these tough times.  
Even $1 can help more than you think 😀🙏

<a href="https://ko-fi.com/gary19gts" target="_blank">
  <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" alt="Buy Me a Coffee at ko-fi.com" style="height: 45px !important; width: 162px !important;">
</a>

Thank you so much for standing with me! ✨  

