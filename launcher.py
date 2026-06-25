import wx
from GUI.MainFrame import MainFrame

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()