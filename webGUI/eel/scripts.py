import eel
from Core import Configuration
from Core.GeneralMethods import *
from Core.webWorker import WebWorker
from webGUI.pythonGUI.ProgressDialog import ProgressDialog

def CheckValues(dictForm):
    errors = ""
    if "selectMode" not in list(dictForm.keys()):
        errors = "Los datos no se recogieron correctamente. Abortando."
        return errors

    if dictForm['selectMode'] == "TraducirUnaLista":
        if "listaUrl" not in list(dictForm.keys()):
            errors += "No se ha escogido una URL para traducir la lista\n"
        elif dictForm["listaUrl"] == "":
            errors += "No se ha escogido una URL para traducir la lista\n"

    elif dictForm['selectMode'] == 'TraducirUnFichero':
        if Configuration.GetPathFicheroListas() == "":
            errors += "No se ha escogido un fichero con las URLs de las Listas\n"

    if Configuration.GetGuardarPdfEn() == "":
        errors += "No se ha seleccionado donde guardar los PDFs generados\n"

    if errors != "":
        errors = errors[:-2]
    return errors


@eel.expose
def GenerateFicheros(dictForm):
    errors = CheckValues(dictForm)
    if errors != "":
        eel.PrintMessage(errors)
        return None

    links = []
    if dictForm['selectMode'] == "TraducirUnaLista":
        links.append(dictForm['listaUrl'])
    elif dictForm['selectMode'] == "TraducirUnFichero":
        f=open(Configuration.GetPathFicheroListas(),'r')
        for link in f.readlines():
            if link.strip() == "":
                continue #The line does not contain a link

            links.append(link.strip())

    pathManual = Configuration.GetManualTranslator()
    ret = Configuration.CheckTranslationFiles()
    if ret&0x01 != 0:
        message = "No se encontró el fichero 'Translations.txt' en config/translation\n"+\
                                       "\n¿Desea crear uno vacio?"
        title = "No se encontró 'Transalations.txt'"
        if YesNoDialog(message, title) == 0:
            f = open(Configuration.GetHistoryTranslator(), 'w', encoding='utf-8')
            f.close()
        else:
            message = "No se encontró el fichero 'Translations.txt' en config/translation"
            ErrorDialog(message)
            return None
    if ret &0x02 != 0:
        message = "No se encontró un fichero con las traducciones manuales\n"+\
                                       "\n¿Desea continuar sin usarlo?"
        title = "Falta Traducciones Manuales"
        resp = YesNoDialog(message, title)
        if resp == 1:
            return None
        pathManual = None

    progress = ProgressDialog("Preparando el navegador...", "OPR Spainer Trabajando", 2+len(links))
    worker = WebWorker(Configuration.GetHistoryTranslator(), pathManual)
    err = worker.CreateWebDriver(dictForm['Browser'], Configuration.GetBrowserVisible())
    if err != "":
        ErrorDialog(err)
        progress.destroy()
        worker.DestroyWebDriver()
        return None

    if progress.WasCancelled():
        worker.DestroyWebDriver()
        return None
    else:
        progress.Update(1)

    worker.PrepareTheBrowser()

    if progress.WasCancelled():
        worker.DestroyWebDriver()
        return None
    else:
        progress.Update(2, "Traduciendo listas [1/{}]".format(len(links)))

    i = 2
    for link in links:
        i += 1
        err = worker.TranslateALink(link, Configuration.GetGuardarPdfEn())
        if err != "":
            resp = YesNoDialog("No se pudo generar la lista\nError: "+err+'\n¿Continuar?')
            if resp != 0:
                progress.Destroy()
                worker.DestroyWebDriver()
                return None
        if progress.WasCancelled():
            return None
        progress.Update(i, "Listas traducidas" if len(link)-i <= -2 else "Traduciendo listas [{}/{}]".format(i-1, len(links)))

    if not progress.WasCancelled():
        progress.Destroy()
    worker.DestroyWebDriver()

    MessageDialog("Se ha finalizado la traducción de listas")
    news = worker.CheckNewTranslations()
    if news != {}:
        resp1 = YesNoDialog("Se han traducido nuevas palabras, ¿desea guardarlas en el traductor?")
        if resp1 == 0:
            worker.SaveTranslations()
        elif resp1 == 1:
            resp2 = YesNoDialog("¿Quieres editar las palabras nuevas para guardarlas como traducciones manuales?")
            if resp2 == 0:
                print("Pendiente habilitar esta opción")
    