import shutil
import os
from cx_Freeze import setup


exePath = "./EXECUTABLE"

if not os.path.exists(exePath):
    os.mkdir(exePath)


# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": [""],
    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
    'includes': ["selenium", "deep_translator", 'pycparser', 'trio', 'trio_websocket', 'urllib3'],
    "include_files": [('config/translation/Translations.txt', 'config/translation/Translations.txt'), 
                      ('listLinks.txt', 'listLinks.txt'),
                      ('config/translation/manualTranslator.txt', 'config/translation/ManualTranslator.txt')],
    "build_exe":"OPRSpainer"
}

setup(
    name="OPRSpainer",
    version="0.5",
    description="Description of the tool",
    options={"build_exe": build_exe_options},
    executables=[{"script": "launcher.py", "base": None}],
)
        
print('Finished')
