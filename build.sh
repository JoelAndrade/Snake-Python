# Runs this script if you want to make a new .exe file
# Need python and pyinstaller installed

pyinstaller app.spec
mv dist/Snake.exe Snake.exe
rm -r __pycache__/ build/ dist/
