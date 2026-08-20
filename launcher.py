import eel
import os

if __name__ == '__main__':
    eel.init(os.path.abspath("webGUI"))
    from webGUI.eel import scripts
    from Core.Configuration import LoadConfiguration

    LoadConfiguration()
    eel.start("home.html",mode="edge", host="localhost", port="8000")
