import os
import eel
import pickle
from Core.GeneralMethods import SaveATranslatorDictionary, YesNoDialog, FolderSelector, TextEntryDialog

global ManualTranslator
global HistoryTranslator
global BrowserVisible
global guardarPdfEn
global pathFicheroListas
global version
ManualTranslator = ".\\config\\manualTranslator.txt"
HistoryTranslator = ".\\config\\Translations.txt"
BrowserVisible = False
guardarPdfEn = ""
pathFicheroListas = ""
version = "1.0.1"

def GetToolVersion():
    global version
    return version

@eel.expose
def GetManualTranslator():
    global ManualTranslator
    return ManualTranslator

@eel.expose
def SetManualTranslator(new_manual):
    global ManualTranslator
    print(new_manual)
    ManualTranslator = new_manual

@eel.expose
def GetHistoryTranslator():
    global HistoryTranslator
    return HistoryTranslator

def SetHistoryTranslator(new_history):
    global HistoryTranslator
    HistoryTranslator = new_history

@eel.expose
def ResetHistoryTranslator():
    global HistoryTranslator
    message = "Se eliminarán todas las traducciones previas del traductor\n"
    message += "Tenga en cuenta que la API para traducir automáticamente tiene un limite de usos al día\n"
    message += "¿Desea proceder?"
    resp =YesNoDialog(message, "Aviso al usuario")
    
    if resp==0:
        if SaveATranslatorDictionary({}, GetHistoryTranslator()):
            return True
        else:
            return False
    return False

@eel.expose
def CreateMaualTranslator():
    global ManualTranslator
    path = FolderSelector("¿Donde crear el traductor manual?", 'config/translation')
    if path != "":
        filename = TextEntryDialog("Por favor, indique el nombre del nuevo traductor Manual", 'Indique el nombre')
        if filename != None:
            filename = filename.strip() +'.txt'
            while os.path.exists(os.path.join(path, filename)) or filename=='.txt':
                filename = TextEntryDialog("Nombre no es correcto. Ya existe o está vacio.\nPor favor, indique el nombre del nuevo traductor Manual", 'Indique el nombre')
                if filename != None:
                    filename = filename.strip() +'.txt'
                else: 
                    filename = '.txt' #So the file creation is aborted
                    break
            if filename != '.txt': #The user introduced a valid name
                if SaveATranslatorDictionary({}, os.path.join(path, filename)):
                    SetManualTranslator(os.path.join(path, filename))
                    return True
    return False


def CheckTranslationFiles():
    error = 0
    if not os.path.exists(GetHistoryTranslator()):
        error += 1<<0

    if not os.path.exists(GetManualTranslator()):
        error += 1<<1

    return error

@eel.expose
def GetBrowserVisible():
    global BrowserVisible
    return BrowserVisible

@eel.expose
def SetBrowserVisible(new_visible):
    global BrowserVisible
    if isinstance(new_visible, bool):
        BrowserVisible = new_visible

@eel.expose
def GetGuardarPdfEn():
    global guardarPdfEn
    return guardarPdfEn

@eel.expose
def SetGuardarPdfEn(folder_path):
    global guardarPdfEn
    guardarPdfEn = folder_path

def GetPathFicheroListas():
    global pathFicheroListas
    return pathFicheroListas

@eel.expose
def SetPathFicheroListas(file_path):
    global pathFicheroListas
    pathFicheroListas = file_path

@eel.expose
def SaveConfiguration():
    data2Save = {}
    data2Save['ManualTranslator'] = GetManualTranslator()
    data2Save['BrowserVisible'] = GetBrowserVisible()
    data2Save['guardarPdfEn'] = GetGuardarPdfEn()

    f = open("config.bin",'wb')
    pickle.dump(data2Save, f)
    f.close()

def LoadConfiguration():
    if os.path.exists("config.bin"):
        f = open("config.bin", 'rb')
        data2Load = pickle.load(f)
        f.close()

        SetManualTranslator(data2Load['ManualTranslator'])
        SetBrowserVisible(data2Load['BrowserVisible'])
        SetGuardarPdfEn(data2Load['guardarPdfEn'])