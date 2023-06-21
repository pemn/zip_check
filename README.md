# zip_check
## 📌 description
This project consist of two independent but related apps:  
 1 - simple Python 🐍 desktop app for checking integrity of all zip files in a folder tree  
 2 - Windows powershell script with a similar purpose but that does not require python runtime
## 🧰 installation (python app)
Requires Winpython or a compatible Python distribution. Basic Python runtime is not sufficient.  
If not already installed, extract latest winpython distribution to the `%APPDATA%` folder.  
Ex.:  
`C:\Users\user\AppData\Roaming\WPy64-31131`  
Download this repository and extract to any folder.  
Recomended (Windows):  
`%APPDATA%\zip_check`  
Ex. (Windows):  
`C:\Users\user\AppData\Roaming\zip_check`
## 📑 usage - Windows - Python
Once both Winpython and the app are setup, double click the zip_check.py file to start.  
If file associations with .py files is not working, double click the .cmd file that will try to autodetect the winpython folder.
## 📑 usage - Windows - Powersheell
Copy the check_zips_ps.bat file in any valid folder and double click. It will check all zips on that folder and its subfolders, then present a csv report.  
## usage - Other OSs
Install a Python distribution compatible with your OS.  
Run the following command or create a shortcut:  
`python zip_check.py`
## 📸 screenshots
### screenshot1
![screenshot1](./assets/zip_check1.png?raw=true)
### screenshot2
![screenshot2](./assets/zip_check2.png?raw=true)
## 💎 License
Apache 2.0
## 📓 Notes
 - Some zip files for testing are included in `test` folder
 - A .html file with this README compiled is included for convenience
 - Only zip files are supported, other compressed formats could be easily included. Fork away!
 - Windows prevents execution of apps in some protected folders such as Downloads, Desktop, Documents. So if you see a blue "This app has been blocked" error message, move the files to a more appropriate folder like `c:\scripts` or `%APPDATA%`.
## 📚 Examples
## 🧩 Compatibility
