import os
import pickle
import eel
import tkinter
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

def YesNoDialog(message, title=''):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    if title == "":
        title = messagebox
    buttonResponse = messagebox.Message(default='yes', icon='question', message = message,
                                        title = title, type='yesno', parent=root).show()
    root.destroy()
    if buttonResponse == 'yes':
        return 0
    elif buttonResponse == 'no':
        return 1
    else:
        return -1

def ErrorDialog(message):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.Message(default='ok', icon='error', message = message,
                        title = "Algo salió mal", type='ok', parent=root).show()
    root.destroy()

def MessageDialog(message, title=""):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    if title == "":
        title = "Información"
    resp = messagebox.Message(default='ok', icon='info', message = message,
                        title = title, type='ok', parent=root).show()
    root.destroy()
    if resp == 'ok':
        return 0
    else:
        return -1


def TextEntryDialog(message, title=""):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    entryText = simpledialog.askstring(title=title, prompt=message, parent=root)
    root.destroy()
    return entryText    

@eel.expose
def FileSelector(title="", startPath="."):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filePath = filedialog.askopenfilename(title=title, initialdir=startPath, parent=root)
    root.destroy()
    return filePath

@eel.expose
def FolderSelector(title="", startPath="."):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    filePath = filedialog.askdirectory(title=title, initialdir=startPath, parent=root)
    root.destroy()
    return filePath

@eel.expose
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

@eel.expose
def SaveATranslatorDictionary(dictionary, dictPath, printConfirmationMessgae = False):
    try:
        f = open(dictPath, 'wb')
    except IOError:
        resp = MessageDialog("No se pudo abrir el fichero en la ruta: \n"+os.path.realpath(dictPath)+\
                                  "\nCierrelo y clique en 'OK'")
        if resp == 0:
            try:
                f = open(dictPath, 'wb')
            except:
                if printConfirmationMessgae:
                    ErrorDialog("No se pudo guardar los cambios porque el traductor ya está abierto")
                return False
        else:
            return False
    except Exception as e:
        if printConfirmationMessgae:
            ErrorDialog(f"No se pudo guardar los cambios.\nError: {e}")
        return False
    
    finally:
        pickle.dump(dictionary, f)
        f.close()
        if printConfirmationMessgae:
            MessageDialog("Se guardaron los cambios correctamente")
        return True