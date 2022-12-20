# Installer Use Guide

### Build Installer for Linux
The build script for linux is tested on Amazon Linux 2.

```
cd <Path to the Source Code>
./installer/pyinstaller/build-linux.sh amazon-emr-serverless-image-cli-linux-x86_64.zip
```

### Build Installer for macOS

```
cd <Path to the Source Code>
./installer/pyinstaller/build-mac.sh amazon-emr-serverless-image-cli-mac-x86_64.zip 3.10.5
```

### Build Executable for windows

#### Build the .exe file.

If you have python3 pre-installed:
```
cd <Path to the Source Code>
./installer/pyinstaller/build-win.bat
```

If you don't have python3 pre-installed, you can either install it by yourself or enter python version as an
input to automatically install.
```
cd <Path to the Source Code>
./installer/pyinstaller/build-win.bat 3.7.9
```
This may require to unblock the python-installation.exe file (The requirement differs in computers).
