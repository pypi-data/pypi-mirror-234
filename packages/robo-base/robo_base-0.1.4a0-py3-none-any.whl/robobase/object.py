#
#
# Object - primary primordal base class 
#
# (c) 2022 - 2023  Mike Knerr
#
#

import os 

## primordal class

class Object(object):
    
     # successive classes override these in their init
     def __init__(self): #,instance="Instance Name"):
         self._id = id(self)
         self._name="Object"
         self._desc="Object - Primary Base Object"
         self._vers="v0.01.07b" # this is the prev dev vers not pypi package vers yet
         self._model = "" # more for derived classes
         self._about="About Object..."
         self._instance_name = ""
         self._debug_flag = False
       
     def whoami(self):
          print(self._name,self._vers,self._model)
     
     def getWhoami(self):
         return str(self._name+" "+self._vers+" "+self._model)
     
     def whoamiStr(self):
         return self.getWhoami()
     
     def getId(self):
         return self._id
     
     def getName(self):
        return self._name

     def getDesc(self):
        return self._desc
    
     def getVersion(self):
        return self._vers
    
     def getVers(self):
        return self._vers
    
     def getAbout(self):
        return self._about
    
     def setName(self,n):
         self._name = n
    
     def setDesc(self,d):
         self._desc = d
         
     def setAbout(self,a):
         self._about = a
    
     # not on the public inteface
     # hard code this one 
     # def setVers(self,v):
     #    self._vers =v
         
     def setDebugOn(self):
         self._debug_flag = True
         
     def setDebugOff(self):
         self._debug_flag = False
         
     #future rem these 2 use set*()
     #def debugOn(self):
     #    self.setDebugOn()
     
     #def debugOff(self):
     #    self.setDebugOff()
         
     #future, maybe rem not specific enough
     def debug(self):
         return (self._debug_flag == True) 
         
     def debugIsOn(self):
         # makes more sense w/ if debugIsOn(): then...
         return (self._debug_flag == True) #test as bool
       
     def isDebugOn(self):
         # backward compat
         return self.debugIsOn()
          #return self.debug()
      
    # the shell commands
     
     def id(self):
         print(self._id)
         
     def name(self):
           print(self._name)

     def desc(self):
        print(self._desc)
    
     def version(self):
        print(self._vers)
    
     def vers(self):
        print(self._vers)
    
     def about(self):
        print(self._about)
        
 
   
