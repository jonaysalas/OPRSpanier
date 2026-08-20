import shutil
import os
import subprocess
from Core.Configuration import GetToolVersion

## Configurable Data
exePath = "./EXECUTABLE"
folders2copy = ['config', 'webGUI']

## End of Configurable Data

command = "pyinstaller "
command += "--distpath {} -y ".format(exePath)
command += "-F " #Onefile

res = input("Should the executable show its console? (Y/N): ")
if res.lower() == "y":
    command += '-c '
else:
    command += '-w '

command += '--collect-data selenium '

if os.path.exists(exePath):
    shutil.rmtree(exePath)
#Edit the file version
shutil.copy("file_version_info.txt", "fvi.txt")

f = open("fvi.txt",'r')
txt = f.read()
f.close()

#Imports the Selenium
command += '--hidden-import selenium.webdriver.chrome.webdriver '
command += '--hidden-import selenium.webdriver.edge.webdriver '
command += '--hidden-import selenium.webdriver.firefox.webdriver '

f = open("fvi.txt",'w')
f.write(txt.replace("#VERSION#",GetToolVersion()))
f.close()

command += "--version-file fvi.txt "
command += "launcher.py"

subprocess.run(command)

#Remove the unnecesary files:
os.remove("fvi.txt")    
shutil.rmtree("build")

#Copy the folders to the executable
for folder in folders2copy:
    if os.path.exists(folder):
        shutil.copytree(folder, os.path.join(exePath, folder))

print('Finished')
