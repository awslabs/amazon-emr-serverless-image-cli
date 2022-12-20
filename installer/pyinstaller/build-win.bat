@echo off
set python_version=%1


echo "Making Folders"
mkdir .build_win\src
mkdir .build_win\output\amazon-emr-serverless-image-cli

echo "Copying Source"
robocopy . .build_win\src /e /XD .build_win
cd .build_win\src
rmdir /s /q scripts
del Makefile
rmdir /s /q venv
rmdir /s /q __pycache__
cd ..

if not "%python_version%"=="" (
    echo "Installing Python3"
    curl "https://www.python.org/ftp/python/%python_version%/python-%python_version%-amd64.exe" --output python_install.exe
    python_install.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
)


echo "Installing Python Libraries"
py -3 -m venv venv
venv\Scripts\pip3.exe install -r src/installer/pyinstaller/requirements.txt
venv\Scripts\pip3.exe install src/

echo "Building Binary"
cd src
echo "custom-image-validation-tool.spec content is:"
..\venv\Scripts\python.exe -m PyInstaller --clean installer\pyinstaller\custom-image-validation-tool-win.spec

mkdir pyinstaller-output
mkdir pyinstaller-output\bin
robocopy /e /move dist pyinstaller-output\bin
cd ..
robocopy /e src\pyinstaller-output output/amazon-emr-serverless-image-cli
robocopy src output/amazon-emr-serverless-image-cli README.md