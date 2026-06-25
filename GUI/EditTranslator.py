# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

import gettext
_ = gettext.gettext

from Core.GeneralMethods import LoadATranslatorDictionary, SaveATranslatorDictionary
from GUI.MultilineTxtDialog import MultilineTextDialog

###########################################################################
## Class TranslatorFrame
###########################################################################

class TranslatorFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"   Editar un traductor   ", pos = wx.DefaultPosition, size = wx.Size( 709,440 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.lblFrame = wx.StaticText( self, wx.ID_ANY, _(u"TypeOfTranslations"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblFrame.Wrap( -1 )

        bSizer2.Add( self.lblFrame, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_grid2 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.m_grid2.CreateGrid( 5, 2 )
        self.m_grid2.EnableEditing( False )
        self.m_grid2.EnableGridLines( True )
        self.m_grid2.EnableDragGridSize( False )
        self.m_grid2.SetMargins( 0, 0 )

        # Columns
        self.m_grid2.SetColSize( 0, 80 )
        self.m_grid2.SetColSize( 1, 1129 )
        self.m_grid2.AutoSizeColumns()
        self.m_grid2.EnableDragColMove( False )
        self.m_grid2.EnableDragColSize( False )
        self.m_grid2.SetColLabelValue( 0, _(u"Texto Original") )
        self.m_grid2.SetColLabelValue( 1, _(u"Texto Traducido") )
        self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.m_grid2.EnableDragRowSize( True )
        self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.m_grid2.SetDefaultCellBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
        self.m_grid2.SetDefaultCellTextColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
        self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer2.Add( self.m_grid2, 1, wx.ALL|wx.EXPAND, 5 )

        self.btnAñadirLineaManual = wx.Button( self, wx.ID_ANY, _(u"Añadir nueva Linea"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.btnAñadirLineaManual, 0, wx.ALL|wx.EXPAND, 5 )

        self.btnDeleteRowManual = wx.Button( self, wx.ID_ANY, _(u"Eliminar Lineas Seleccionadas"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.btnDeleteRowManual, 0, wx.ALL|wx.EXPAND, 5 )


        fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer2.AddGrowableCol( 0 )
        fgSizer2.AddGrowableCol( 1 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.buttonSaveChanges = wx.Button( self, wx.ID_ANY, _(u"Guardar"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.buttonSaveChanges, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.btnCancelClose = wx.Button( self, wx.ID_ANY, _(u"Cancelar"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.btnCancelClose, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer2.Add( fgSizer2, 0, wx.EXPAND, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.CloseNoSave )
        self.m_grid2.Bind( wx.grid.EVT_GRID_CELL_CHANGED, self.CheckAndResize )
        self.m_grid2.Bind( wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.EditCell )
        self.btnAñadirLineaManual.Bind( wx.EVT_BUTTON, self.añadirLinea )
        self.btnDeleteRowManual.Bind( wx.EVT_BUTTON, self.DeleteRows )
        self.buttonSaveChanges.Bind( wx.EVT_BUTTON, self.SaveChanges )
        self.btnCancelClose.Bind( wx.EVT_BUTTON, self.CloseNoSave )

        # Useful variables
        self.translatorFilePath = ""
        self.parent = parent
        self.allTheOriginalTexts = [] #List of texts of the first column of the grid to avoid duplicates
        self.invisibleDict = {} #So we dont have to show the full translator, we can show just the new lines, for example

        #Method to be called always when created the frame
        self.m_grid2.AutoSizeColumns()

    def __del__( self ):
        pass

    
    # Methods not related with events
    def ConfigureForManual(self, translatorPath):
        self.lblFrame.SetLabelText("Traductor Manual")
        self.translatorFilePath = translatorPath

        allTranslations = LoadATranslatorDictionary(translatorPath)
        
        # Because is the manual, each key has a twin ending in ":", so remove them to make them invisible to the end-user
        for key in list(allTranslations.keys()):
            if key.endswith(':'):
                del allTranslations[key]

        sortedKeys = list(allTranslations.keys())
        sortedKeys.sort()

        row = 0
        for key in sortedKeys:
            if row == self.m_grid2.GetNumberRows():
                self.m_grid2.AppendRows(1)
            self.m_grid2.SetCellValue(row, 0, key)
            self.m_grid2.SetCellValue(row, 1, allTranslations[key])
            self.allTheOriginalTexts.append(key)
            row += 1
        self.m_grid2.AutoSizeColumns()

    def ConfigureForHistory(self, historyTranslator):
        self.lblFrame.SetLabelText("Histórico de traducciones")
        self.translatorFilePath = historyTranslator

        allTranslations = LoadATranslatorDictionary(historyTranslator)

        sortedKeys = list(allTranslations.keys())
        sortedKeys.sort()

        row = 0
        for key in sortedKeys:
            if row == self.m_grid2.GetNumberRows():
                self.m_grid2.AppendRows(1)
            self.m_grid2.SetCellValue(row, 0, key)
            self.allTheOriginalTexts.append(key)
            self.m_grid2.SetCellValue(row, 1, allTranslations[key])
            row += 1

        #The history does not allow to add new lines, only the Found Ones
        self.btnAñadirLineaManual.Hide()
        self.m_grid2.AutoSizeColumns()

    def ConfigureEditNewTranslations(self, traductorPath, new_dict):
        self.lblFrame.SetLabelText("Traductor Manual")
        self.translatorFilePath = traductorPath

        self.invisibleDict = LoadATranslatorDictionary(traductorPath)
        
        sortedKeys = list(new_dict.keys())
        sortedKeys.sort()

        row = 0
        for key in sortedKeys:
            if row == self.m_grid2.GetNumberRows():
                self.m_grid2.AppendRows(1)
            self.m_grid2.SetCellValue(row, 0, key)
            self.m_grid2.SetCellValue(row, 1, new_dict[key])
            self.allTheOriginalTexts.append(key)
            row += 1
        self.m_grid2.AutoSizeColumns()

    def CreateTranslatorManualFromGrid(self):
        base_dict = self.CreateTranslatorFromGrid() #To avoid double code
        for key in list(base_dict.keys()):
            if not key.endswith(':'): #Maybe is needed to add the key with ':' at the end
                if (key+':') not in list(base_dict.keys()): #Missing the version with ':', so we create it
                    base_dict[key+':'] = base_dict[key]+':'
        
        return base_dict

    def CreateTranslatorFromGrid(self):
        new_dict = self.invisibleDict #So if there is some translations we are not seeing, we still save them
        row = 0
        maxRows = self.m_grid2.GetNumberRows()
        while row < maxRows:
            orig = self.m_grid2.GetCellValue(row,0)
            trad = self.m_grid2.GetCellValue(row,1)

            if not (orig == trad == "") : #The row is NOT empty
                new_dict[orig] = trad
            
            row += 1
        
        return new_dict

    # Virtual event handlers, override them in your derived class
    def CheckAndResize( self, event ):
        selectedCell = self.m_grid2.GetGridCursorCoords()
        if selectedCell[1] == 0: #We only make sure the original text is not repeated
            value = self.m_grid2.GetCellValue(selectedCell).strip()
            if value != "" and value in self.allTheOriginalTexts:
                dialog =  wx.MessageDialog(self, "El siguiente texto original ya existe en otra linea de la tabla. ¡No puede haber duplicados en la primera columna!\n"+value, "Aviso al usuario", style = wx.OK|wx.ICON_ERROR|wx.STAY_ON_TOP)
                dialog.ShowModal()
                self.m_grid2.SetCellValue(selectedCell, "")
                self.m_grid2.SetGridCursor(selectedCell)
            elif value != "":
                self.allTheOriginalTexts.append(value)
        self.m_grid2.AutoSizeColumns()
        self.Update()

    def EditCell( self, event ):
        r, c = self.m_grid2.GetGridCursorCoords()
        prev_Val = self.m_grid2.GetCellValue(r, c)
        dialog = MultilineTextDialog(self, "Edita el texto de la celda")
        dialog.SetTxtCtrlValue(prev_Val)
        if dialog.ShowModal() == wx.ID_OK:
            self.m_grid2.SetCellValue(r,c, dialog.GetTxtCtrlValue())
        self.m_grid2.AutoSizeColumns()
        dialog.Destroy()


    def añadirLinea( self, event ):
        self.m_grid2.AppendRows(1)
        self.m_grid2.AutoSizeColumns()
        self.Update()

    def DeleteRows( self, event ):
        #I want to allow the user to select just one cell instead of all the row
        cells = self.m_grid2.GetSelectedCells()
        if len(cells) != 0:
            rows = []
            for cell in cells:
                row = cell[0]
                if row not in rows:
                    rows.append(row)
        else:
            rows = [self.m_grid2.GetGridCursorRow()]
        
        rows.sort()
        rows = rows[::-1] #To start deleting from the bottom to top, so the index numbers are consistent
        for row in rows:
            value = self.m_grid2.GetCellValue(row, 0).strip()
            self.m_grid2.DeleteRows(row)
            self.allTheOriginalTexts.remove(value)
        
        self.m_grid2.AutoSizeColumns()
        self.Update()

    def SaveChanges( self, event ):
        dialog =  wx.MessageDialog(self, "Se guardará el traductor actual, sobreescribiendo el origianl\n¿Continuar?", "Aviso al usuario", style = wx.YES_NO|wx.ICON_QUESTION|wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            new_trad = {}
            if 'Manual' in self.lblFrame.GetLabelText():
                new_trad = self.CreateTranslatorManualFromGrid()
            else:
                new_trad = self.CreateTranslatorFromGrid()
            SaveATranslatorDictionary(new_trad, self.translatorFilePath)
            dialog =  wx.MessageDialog(self, "El traductor se guardó correctamente", "Aviso al usuario", style = wx.OK|wx.ICON_INFORMATION|wx.STAY_ON_TOP)
        dialog.Destroy()
        self.parent.Show()
        self.Destroy()

    def CloseNoSave( self, event ):
        self.parent.Show()
        self.Destroy()


