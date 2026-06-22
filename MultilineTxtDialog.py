# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MultilineTextDialog
###########################################################################

class MultilineTextDialog ( wx.Dialog ):

    def __init__( self, parent, title ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.STAY_ON_TOP )

        self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 600,-1 ), wx.TE_MULTILINE|wx.TE_RICH2 )
        bSizer3.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND, 5 )

        fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer3.AddGrowableCol( 0 )
        fgSizer3.AddGrowableCol( 1 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.btnOk = wx.Button( self, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer3.Add( self.btnOk, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.btnCancel = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer3.Add( self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer3.Add( fgSizer3, 0, wx.EXPAND, 5 )


        self.SetSizer( bSizer3 )
        self.Layout()
        bSizer3.Fit( self )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.returnCancel )
        self.btnOk.Bind( wx.EVT_BUTTON, self.returnOk )
        self.btnCancel.Bind( wx.EVT_BUTTON, self.returnCancel )


    def __del__( self ):
        self.EndModal(wx.ID_CANCEL)

    # Method not related with events
    def SetTxtCtrlValue(self, value):
        self.m_textCtrl2.SetValue(value)
    
    def GetTxtCtrlValue(self):
        return self.m_textCtrl2.GetValue()

    # Virtual event handlers, override them in your derived class
    def returnOk( self, event ):
        self.EndModal(wx.ID_OK)

    def returnCancel( self, event ):
        self.EndModal(wx.ID_CANCEL)


