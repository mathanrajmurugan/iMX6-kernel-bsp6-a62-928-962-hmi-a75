import sys, getopt
import wx
import wx.wizard as wiz
import j8_images as images
import config as conf
import os.path


#----------------------------------------------------------------------

dtsfile = ''


def makePageTitle(wizPg, title):

    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer




class CommonPage(wiz.PyWizardPage):

    def __init__(self, parent, title, wiz_image):

        wiz.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.bSelected=""
        self.sizer = makePageTitle(self, title)
        self.txt = title
        self.wi_img = wiz_image
   
    def SetNext(self, next):

        self.next = next


    def SetPrev(self, prev):

        self.prev = prev


    def GetNext(self):

        return self.next


    def GetPrev(self):

        return self.prev



    def GetSelBoard(self):

        return self.bSelected
            
     
    def SetSelBoard(self, bsel):

        self.bSelected=bsel
   
   
    def GetBitmap(self):
        return self.wi_img.GetBitmap()

        

#----------------------------------------------------------------------


class BoardSelectPage(CommonPage):

    def __init__(self, parent, title, bsel, wi_img):

        CommonPage.__init__(self, parent, title, wi_img)
        
        self.__bsel = bsel 
        
        self.sizer.Add(wx.StaticText(self, -1, """
Select an available board configuration."""))

        self.board_combo = wx.ComboBox(self, -1, style=wx.CB_READONLY)
        self.board_combo.SetItems(self.__bsel.getBoardList())
        self.sizer.Add(self.board_combo, 0, wx.ALL, 5) 
                     
        self.txt_processor = wx.StaticText(self, -1, "Processor: ");
        self.txt_memory = wx.StaticText(self, -1, "Memory: ");
        self.txt_emmc = wx.StaticText(self, -1, "eMMC: ");
        self.txt_j8 = wx.StaticText(self, -1, "J8: ");
        self.txt_temp = wx.StaticText(self, -1, "Temp: ");
        
        self.board_combo.SetSelection(0)
        item = self.board_combo.GetStringSelection()
        self.txt_processor.SetLabelText("processor: %s" % self.__bsel.getProcessor(item))
        self.txt_memory.SetLabelText("Memory: %s" % self.__bsel.getMemory(item))
        self.txt_emmc.SetLabelText("eMMC: %s" % self.__bsel.getEMMC(item))
        self.txt_j8.SetLabelText("J8: %s" % self.__bsel.getJ8(item))
        self.txt_temp.SetLabelText("Temp: %s" % self.__bsel.getTemp(item))
        self.SetSelBoard(item)
        self.UpdateBoard()
        
        self.sizer.Add(self.txt_processor, 0, wx.ALL, 5)
        self.sizer.Add(self.txt_memory, 0, wx.ALL, 5)
        self.sizer.Add(self.txt_emmc, 0, wx.ALL, 5)
        self.sizer.Add(self.txt_j8, 0, wx.ALL, 5)
        self.sizer.Add(self.txt_temp, 0, wx.ALL, 5)
        
        self.Bind(wx.EVT_COMBOBOX, self.on_board_combo_changed)      
               
    
    def on_board_combo_changed(self, event):
    
        item = self.board_combo.GetStringSelection()
        self.txt_processor.SetLabelText("processor: %s" % self.__bsel.getProcessor(item))
        self.txt_memory.SetLabelText("Memory: %s" % self.__bsel.getMemory(item))
        self.txt_emmc.SetLabelText("eMMC: %s" % self.__bsel.getEMMC(item))
        self.txt_j8.SetLabelText("J8: %s" % self.__bsel.getJ8(item))
        self.txt_temp.SetLabelText("Temp: %s" % self.__bsel.getTemp(item))
        self.SetSelBoard(item)
        self.UpdateBoard()
               

    def UpdateBoard(self):
        # update all other pages
        page = self
        while page.next != None:
            page = page.GetNext()
            page.SetSelBoard(self.GetSelBoard())
            
            




#----------------------------------------------------------------------

class PortConfigPage(CommonPage):

    def __init__(self, parent, title, nPort, conf_file, wi_img):

        CommonPage.__init__(self, parent, title, wi_img)

        self.__nPort = nPort
        self.__conf = conf.PortConfiguration(conf_file)
        
        self.__nSection = self.__conf.maxNumOfMultiSelection(nPort)        
        self.__nMaxConf = self.__conf.maxGlobalNumOfConfiguration(nPort)
        
        self.txt_title = wx.StaticText(self, -1, "Select the configuration for the port %s for board %s." % (self.__nPort, self.GetSelBoard()))
        self.sizer.Add(self.txt_title, 0, wx.ALL, 5)
        
        self.sect_list = []
        self.conf_list = []
        
        for s in range(self.__nSection):
            self.conf_list.append([])
            
            for c in range(self.__nMaxConf):
                self.conf_list[s].append("item %d" % c)  
            
            rbox = wx.RadioBox(self, choices = self.conf_list[s], style = wx.RA_SPECIFY_ROWS)
            self.sect_list.append(rbox)
            self.sizer.Add(rbox, 0, wx.EXPAND|wx.ALL, 5)


    def SetSelBoard(self, bsel):

        CommonPage.SetSelBoard(self, bsel)


    def GetPortID(self):
    
        return self.__nPort
        
        
    def UpdateBoard(self):
    
       self.txt_title.SetLabelText("Configuration for the port %s for board %s 1." % (self.__nPort, self.bSelected))
       
       for s in range(self.__nSection):
       
            rbox = self.sect_list[s]
            self.conf_list[s] = self.__conf.getConfListPerSection(self.__nPort, self.GetSelBoard(), s)
            
            for c in range(rbox.GetCount()):
                rbox.ShowItem(c, False)
                
            for i, l in enumerate(self.conf_list[s]):
                rbox.SetString(i, self.conf_list[s][i])
                rbox.ShowItem(i, True)
                
         
    def GetChoiceIndex(self, section):
    
        rbox = self.sect_list[section]
        return rbox.GetSelection()


    def GetChoiceText(self, section):
    
        rbox = self.sect_list[section]
        return rbox.GetItemLabel(rbox.GetSelection())




#----------------------------------------------------------------------


class TestPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)

        self.__bsel = conf.BoardSelector("./blist.conf")
        
        self.__DTSconf = conf.DTSConfigurator("./dts.list", "./dts.conf")
        
        self.dts_data = ""

        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGED, self.OnWizPageChanged)
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGING, self.OnWizPageChanging)
        self.Bind(wiz.EVT_WIZARD_CANCEL, self.OnWizCancel)
        self.Bind(wiz.EVT_WIZARD_FINISHED, self.OnWizFinished)
        self.OnRunWizard(self.__bsel)
         

    def OnWizPageChanging(self, evt):

        page = evt.GetPage()

        if evt.GetDirection():          
            dir = "forward"
        else:       
            dir = "backward"    
        
        #print "OnWizPageChanging: %s, %s\n" % (dir, page.__class__)
        
        
    def OnWizPageChanged(self, evt):

        page = evt.GetPage()

        if evt.GetDirection():
            page.UpdateBoard()
            dir = "forward"
        else:
            dir = "backward"
        
        #print "OnWizPageChanged: %s, %s\n" % (dir, page.__class__)


    def OnWizCancel(self, evt):

        page = evt.GetPage()
        #print "OnWizCancel: %s\n" % page.__class__

        # Show how to prevent cancelling of the wizard.  The
        # other events can be Veto'd too.
        #if page is self.page1:
        #    wx.MessageBox("Cancelling on the first page has been prevented.", "Sorry")
        #   evt.Veto()


    def OnWizFinished(self, evt):

        page = self.page1
        
        dts=""
        while page.next != None:
            page = page.GetNext()
            
            lst = self.__DTSconf.getFullTagsNameFromConfig(page.GetPortID(), page.GetChoiceText(0))
            for tag in lst:
                node = self.__DTSconf.getDTSnodeFromTag (tag)
                if ( node != "" ):
                    dts = "%s\n\n%s\n" % (dts, node)
            
            
        file = open("./dts_header.txt", "r") 
        header = file.read()
        file.close
        dts = "%s\n%s" % (header, dts)
        
        self.dts_data = dts       
                    
        #print "OnWizFinished\n"


    def OnRunWizard(self, bsel):

        # Create the wizard and the pages
        wizard = wiz.Wizard(self, -1, "SBC J8 Expantion Connector Configurator", images.sbc_j8.GetBitmap())

	    # Board Selection
        page1 = BoardSelectPage(wizard, "Board Selection", self.__bsel, images.sbc_j8)
        wizard.FitToPage(page1)

        page2 = PortConfigPage(wizard, "Config Port - 1", 1, "./ports.conf", images.sbc_j8_p1)
        page3 = PortConfigPage(wizard, "Config Port - 2", 2, "./ports.conf", images.sbc_j8_p2)
        page4 = PortConfigPage(wizard, "Config Port - 3", 3, "./ports.conf", images.sbc_j8_p3)
        page5 = PortConfigPage(wizard, "Config Port - 4", 4, "./ports.conf", images.sbc_j8_p4)
        page6 = PortConfigPage(wizard, "Config Port - 5", 5, "./ports.conf", images.sbc_j8_p5)
        page7 = PortConfigPage(wizard, "Config Port - 6", 6, "./ports.conf", images.sbc_j8_p6)
        page8 = PortConfigPage(wizard, "Config Port - 7", 7, "./ports.conf", images.sbc_j8_p7)
        page9 = PortConfigPage(wizard, "Config Port - 8", 8, "./ports.conf", images.sbc_j8_p8)
        page10 = PortConfigPage(wizard, "Config Port - 9", 9, "./ports.conf", images.sbc_j8_p9)
        
        self.page1 = page1

        # Use the convenience Chain function to connect the pages
        page1.SetNext(page2)
        page2.SetPrev(page1)
        page2.SetNext(page3)
        page3.SetPrev(page2)
        page3.SetNext(page4)
        page4.SetPrev(page3)
        page4.SetNext(page5)
        page5.SetPrev(page4)
        page5.SetNext(page6)
        page6.SetPrev(page5)
        page6.SetNext(page7)
        page7.SetPrev(page6)
        page7.SetNext(page8)
        page8.SetPrev(page7)
        page8.SetNext(page9)
        page9.SetPrev(page8)
        page9.SetNext(page10)
        page10.SetPrev(page9)

        wizard.GetPageAreaSizer().Add(page1)
        
        if wizard.RunWizard(page1):
        
            if ( os.path.isfile(dtsfile) == True ):
                retCode = wx.MessageBox("DTS destination file already exists. Do you want to overwrite it?","DTS File Info",  wx.YES_NO | wx.ICON_QUESTION)
                
                if ( retCode == wx.ID_NO ):
                
                    wx.MessageBox("Wizard not completed", "SBD J8 Config")
                    sys.exit ()
                    
            file = open(dtsfile, "w") 
            file.write(self.dts_data)
            file.close
            
            if ( os.path.isfile(dtsfile) == True ):
                wx.MessageBox("Wizard completed successfully", "SBD J8 Config")
            else:
                wx.MessageBox("Wizard not completed, impossible to create dts file", "SBD J8 Config")
            
        else:
        
            wx.MessageBox("Wizard was cancelled", "SBD J8 Config")





    
#----------------------------------------------------------------------
if __name__ == "__main__":

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,"hd:",["dts="])
    except getopt.GetoptError:
        print 'SBC_J8.py -d <dts file output>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'SBC_J8.py -d <dts file output>'
            sys.exit()
        elif opt in ("-d", "--dts"):
            dtsfile = arg
    
    if ( dtsfile == "" ):
        print ("DTS Output file do not specified")
        sys.exit()
    print ("DTS Output file is %s" % dtsfile)


    app = wx.App(0)
   
    frame = wx.Frame(None)
    panel = TestPanel(frame)
        
    frame.Show()
    #app.MainLoop()
