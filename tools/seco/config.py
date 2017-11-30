import ConfigParser
import re


class BoardSelector:

    def __init__(self, fileName):
    
        self.__boardList = 0;
        self.__Config = ConfigParser.ConfigParser()
        self.__fileName = fileName
        
        
    def getBoardList(self):
        self.__Config.read(self.__fileName)
        sections = self.__Config.sections()
        return sections
        
    
    def getProcessor(self, board):
        self.__Config.read(self.__fileName)
        return self.__Config.get(board, 'processor')
   
        
    def getMemory(self, board):
        self.__Config.read(self.__fileName)
        return self.__Config.get(board, 'memory')
        

    def getEMMC(self, board):
        self.__Config.read(self.__fileName)
        return self.__Config.get(board, 'eMMC')

       
    def getJ8(self, board):
        self.__Config.read(self.__fileName)
        return self.__Config.get(board, 'J8')


    def getTemp(self, board):
        self.__Config.read(self.__fileName)
        return self.__Config.get(board, 'temp')



#----------------------------------------------------------------------



class PortConfiguration:

    def __init__(self, fileName):
    
        self.__Config = ConfigParser.ConfigParser()
        self.__fileName = fileName
        self.__Config.read(self.__fileName)
     
        
    def getConfText(self, portID, board):
    
        lst=[]
        sections = self.__Config.sections()
        conf=self.__Config.get("PORT%d" % portID, board)
        return conf
        

    def getConfList(self, portID, board):
        conf = self.getConfText(portID, board)
        lst=conf.split(",")
        for i, l in enumerate(lst):
            lst[i] = lst[i].lstrip(' ')
        return lst
        
        
    def maxNumOfMultiSelection(self, portID):
    	multisel = 0
    	item = dict(self.__Config.items("PORT%d" % portID))
        for it in item:
    	    conf = self.getConfText(portID, it)
    	    length = len(conf.split("|"))
    	    if ( length > multisel ):
    	        multisel = length
        return multisel
        
    
    def maxNumOfConfiguration(self, portID, boad):
        conf = self.getConfText(portID, board)
        lst=conf.split(",")
        nconf = len(lst)
        return nconf
        
        
    def maxGlobalNumOfConfiguration(self, portID):
        multisel = 0
        nconf = 0
    	item = dict(self.__Config.items("PORT%d" % portID))
        for it in item:
    	    confs = self.getConfText(portID, it)
    	    list_conf = confs.split("|")
    	    for lc in list_conf:
    	        n = len(lc.split(","))
    	        if ( n > nconf ):
    	            nconf = n
        return nconf
        
        
    def getConfListPerSection(self, portID, board, section):
        sconf = self.getConfText(portID, board)
        lsec=sconf.split("|")
        if ( len(lsec) < section ):
            return []
        conf=lsec[section]
        lst=conf.split(",")
        for i, l in enumerate(lst):
            lst[i] = lst[i].lstrip(' ')
        return lst




#----------------------------------------------------------------------

class DTSConfigurator:

    def __init__(self, fileConfig, fileDTSport):
    
        self.__Config = ConfigParser.ConfigParser()
        self.__fileConfig = fileConfig
        self.__fileDTSport = fileDTSport
        self.__Config.read(self.__fileConfig)
        
        
    def getTagsFromConfig(self, portID, txtConfig):
    
        port = "PORT%d" % portID     
        lst = self.__Config.get(port, txtConfig)
        return lst.split('|')
        
        
    def getFullTagsNameFromConfig(self, portID, txtConfig):
    
        port = "PORT%d" % portID
        lst = self.__Config.get(port, txtConfig)
        lst = lst.split('|')
        for i in range(len(lst)):
            lst[i] = port + '_' + lst[i]
        return lst
        
      
    def getDTSnodeFromTag(self, tag):
        
        if ( tag.find("none") != -1 ):
            return ""
            
        tag_open = "[%s]" % tag
        tag_close = "[/%s]" % tag
        
        file = open(self.__fileDTSport, "r") 
        dts=file.read()
        file.close()
        
        nodel = re.search(r"{0}(.*){1}".format(re.escape(tag_open), re.escape(tag_close)), dts, flags=re.MULTILINE|re.DOTALL)
        node = nodel.group(1)
        
        return node     
        
        
