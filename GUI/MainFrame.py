# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import os
from Core.webWorker import WebWorker

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"    - OPR Spainer -    "), pos = wx.DefaultPosition, size = wx.Size( 500,358 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.configMenu = wx.Menu()
        self.config_dictionary = wx.MenuItem( self.configMenu, wx.ID_ANY, _(u"Seleccionar Traducciones Manuales"), wx.EmptyString, wx.ITEM_NORMAL )
        self.configMenu.Append( self.config_dictionary )

        self.config_browserVisibility = wx.MenuItem( self.configMenu, wx.ID_ANY, _(u"Ocultar Navegador: ON"), wx.EmptyString, wx.ITEM_NORMAL )
        self.configMenu.Append( self.config_browserVisibility )

        self.m_menubar1.Append( self.configMenu, _(u"Config") )

        self.SetMenuBar( self.m_menubar1 )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"  Entradas de Lista(s)  ") ), wx.VERTICAL )

        self.radioUrl = wx.RadioButton( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Traducir una lista de una URL"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer2.Add( self.radioUrl, 0, wx.ALL, 5 )

        self.txtCtrl_listaUrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer2.Add( self.txtCtrl_listaUrl, 0, wx.ALL|wx.EXPAND, 5 )

        self.radioFichero = wx.RadioButton( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Traducir varias listas de un fichero .txt con URLs"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer2.Add( self.radioFichero, 0, wx.ALL, 5 )

        self.filePath_ListasURL = wx.FilePickerCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, _(u"Selecciona el .txt"), _(u"*.txt"), wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        sbSizer2.Add( self.filePath_ListasURL, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer1.Add( sbSizer2, 0, wx.EXPAND|wx.ALL, 5 )

        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"   Configuración para Generar   ") ), wx.VERTICAL )

        fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer2.AddGrowableCol( 1 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.lblBrowser = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Utilizar buscador: "), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblBrowser.Wrap( -1 )

        fgSizer2.Add( self.lblBrowser, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        choiceBrowsersChoices = [ _(u"Firefox"), _(u"Google Chrome"), _(u"Edge") ]
        self.choiceBrowsers = wx.Choice( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choiceBrowsersChoices, 0 )
        self.choiceBrowsers.SetSelection( 0 )
        fgSizer2.Add( self.choiceBrowsers, 0, wx.ALL|wx.EXPAND, 5 )


        sbSizer3.Add( fgSizer2, 1, wx.EXPAND, 5 )

        self.lblRutaPdfs = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Generar PDFs en:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblRutaPdfs.Wrap( -1 )

        sbSizer3.Add( self.lblRutaPdfs, 0, wx.ALL, 5 )

        self.dirPdfs = wx.DirPickerCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, _(u"Selecciona Carpeta Destino"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        sbSizer3.Add( self.dirPdfs, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer1.Add( sbSizer3, 0, wx.ALL|wx.EXPAND, 5 )

        self.btnGenerarPDFs = wx.Button( self, wx.ID_ANY, _(u"Generar Listas"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.btnGenerarPDFs, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.ConfigureTranslator, id = self.config_dictionary.GetId() )
        self.Bind( wx.EVT_MENU, self.toogleBrowserVisibility, id = self.config_browserVisibility.GetId() )
        self.btnGenerarPDFs.Bind( wx.EVT_BUTTON, self.startGeneration )

        # Useful Variables
        self.BrowserVisibility = False
        self.pathManualTranslator = ""
        self.pathTranslations = "config/translation/Translations.txt"

    def __del__( self ):
        pass

    #Methods not related with events
    def checkTranslationsFiles(self):
        error = 0
        if not os.path.exists(self.pathTranslations):
            error += 1<<0

        if not os.path.exists(self.pathManualTranslator):
            error += 1<<1

        return error
    
    def CheckValues(self):
        errors = ""
        if self.radioUrl.GetValue() and self.txtCtrl_listaUrl.GetValue() == "":
            errors += "No se ha escogido una URL para traducir la lista\n"
        elif self.radioFichero.GetValue() and self.filePath_ListasURL.GetPath() == "":
            errors += "No se ha escogido un fichero con las URLs de las Listas\n"
        
        if self.dirPdfs.GetPath() == "":
            errors += "No se ha seleccionado donde guardar los PDFs generados"
        
        if errors != "":
            dialog = wx.MessageDialog(self, errors, style = wx.OK|wx.ICON_ERROR|wx.STAY_ON_TOP)
            dialog.ShowModal()
            dialog.Destroy()

    # Virtual event handlers, override them in your derived class
    def ConfigureTranslator( self, event ):
        dialog = wx.FileDialog(self, "Selecciona el fichero", wildcard='*.txt', style = wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            self.pathManualTranslator = dialog.GetPath()
        dialog.Destroy()

    def toogleBrowserVisibility( self, event ):
        self.BrowserVisibility = not self.BrowserVisibility

        self.config_browserVisibility.SetItemLabel("Ocultar Navegador: {}".format('OFF' if self.BrowserVisibility else 'ON'))

    def startGeneration( self, event ):
        if not self.CheckValues():
            return None
        #First, determine if we translated a link or a bunch of links
        links = []
        if self.radioUrl.GetValue() == True:
            #Translate just a link
            links.append(self.txtCtrl_listaUrl.GetValue())
        elif self.radioFichero.GetValue() == True:
            #Translate a bunch of links from a file
            f = open(self.filePath_ListasURL.GetPath(), 'r', encoding='utf-8')
            for link in f.readlines():
                if link.strip() == "":
                    continue #The line does not contain a link
                
                #Add the link to the list
                links.append(link.strip())
        
        pathManual = self.pathManualTranslator
        ret = self.checkTranslationsFiles()
        if ret&0x01 != 0:
            dialog =  wx.MessageDialog(self, "No se encontró el fichero 'Translations.txt' en config/translation\n"+\
                                       "\n¿Desea crear uno vacio?", "Falta Translations.txt", style = wx.YES_NO|wx.ICON_QUESTION|wx.STAY_ON_TOP)
            if dialog.ShowModal() == wx.ID_YES:
                f = open(self.pathTranslations, 'w', encoding='utf-8')
                f.close()
            else:
                dialog2 = wx.MessageDialog(self, "No se encontró el fichero 'Translations.txt' en config/translation", style = wx.OK|wx.ICON_ERROR|wx.STAY_ON_TOP)
                dialog2.ShowModal()
                dialog2.Destroy()
                dialog.Destroy()
                return None
            
            dialog.Destroy()
            
        
        if ret&0x02 != 0:
            dialog =  wx.MessageDialog(self, "No se encontró un fichero con las traducciones manuales\n"+\
                                       "\n¿Desea continuar sin usarlo?", "Falta Traducciones Manuales", style = wx.YES_NO|wx.ICON_QUESTION|wx.STAY_ON_TOP)
            if dialog.ShowModal() == wx.ID_NO:
                dialog.Destroy()
                return None
            
            dialog.Destroy()
            pathManual = None
        
        progressDialog = wx.ProgressDialog("OPR Spainer trabajando...", "Preparando el navegador...", maximum=2+len(links), style = wx.PD_SMOOTH|wx.PD_CAN_ABORT|wx.PD_ELAPSED_TIME)
        worker = WebWorker(self.pathTranslations, pathManual)
        err = worker.CreateWebDriver(self.choiceBrowsers.GetStringSelection(), self.BrowserVisibility)
        if err != "":
            dialog = wx.MessageDialog(self, err, style = wx.OK|wx.ICON_ERROR|wx.STAY_ON_TOP)
            dialog.ShowModal()
            dialog.Destroy()
            progressDialog.Destroy()
            worker.DestroyWebDriver()
            return None
        
        if progressDialog.WasCancelled():
            progressDialog.Destroy()
            worker.DestroyWebDriver()
            return None
        else:
            progressDialog.Update(1)
        
        worker.PrepareTheBrowser()
        if progressDialog.WasCancelled():
            progressDialog.Destroy()
            worker.DestroyWebDriver()
            return None
        else:
            progressDialog.Update(2, "Traduciendo listas [1/{}]".format(len(links)))
        
        i = 2
        for link in links:
            i += 1
            err = worker.TranslateALink(link, self.dirPdfs)
            if err != "":
                dialog = wx.MessageDialog(self, "No se pudo generar la lista\nError: "+err+'\n¿Continuar?', style = wx.YES_NO|wx.ICON_ERROR|wx.STAY_ON_TOP)
                if dialog.ShowModal() != wx.ID_YES:
                    dialog.Destroy()
                    progressDialog.Destroy()
                    worker.DestroyWebDriver()
                    return None
                
                dialog.Destroy()
            
            progressDialog.Update(i, "Listas traducidas" if len(link)-i <= -2 else "Traduciendo listas [{}/{}]".format(i-1, len(links)))
        
        progressDialog.Destroy()
        worker.DestroyWebDriver()

        dialog = wx.MessageDialog(self, "Se ha finalizado la traducción de listas", style = wx.OK|wx.ICON_ERROR|wx.STAY_ON_TOP)    
        dialog.ShowModal()
        
        news = worker.CheckNewTranslations()
        if news != {}:
            dialog = wx.MessageDialog(self, "Se han traducido nuevas palabras, ¿desea guardarlas en el traductor?", style = wx.YES_NO|wx.ICON_ERROR|wx.STAY_ON_TOP)    
            if dialog.ShowModal() == wx.ID_YES:
                worker.SaveTranslations()
        


