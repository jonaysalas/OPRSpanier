import eel

if __name__ == '__main__':
    eel.init("webGUI")
    from webGUI.eel import scripts
    from Core.Configuration import LoadConfiguration

    LoadConfiguration()
    eel.start("home.html")