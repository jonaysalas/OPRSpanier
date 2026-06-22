import os
import pickle
import wx

def LoadATranslatorDictionary(dictPath):
    tmpDict = {}
    if os.path.exists(dictPath):
        try:
            f = open(dictPath, 'rb')
            tmpDict = pickle.load(f)
            f.close()
        except:
            None #Something went wrong, maybe the file is empty
    return tmpDict

def SaveATranslatorDictionary(dictionary, dictPath):
    try:
        f = open(dictPath, 'wb')
    except IOError:
        dialog = wx.MessageDialog(None, "No se pudo abrir el fichero en la ruta: \n"+os.path.realpath(dictPath)+\
                                  "\nCierrelo y clique en 'OK'", style = wx.OK|wx.ICON_ERROR|wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_OK:
            try:
                f = open(dictPath, 'wb')
            except:
                return False
        else:
            return False
    except:
        return False
    
    finally:
        pickle.dump(dictionary, f)
        f.close()
        return True