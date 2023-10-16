#
#
# system - system related classes & functions
#
# (c) 2022 - 2023  Mike Knerr
#
#

## other promordal classes

from .object import Object
import os

class System(Object):
    # so far just a wrapper for some 
    # common shell commands from underlying OS/HW system
    # not the robots interface shell yet

    def __init__(self): #v0.07
        super(System, self).__init__()
         
        self._name = "System"
        self._desc = "OS/HW System shell functions"
        self._vers = "v0.01.01a"  
        self._model = ""
        
    def kernelVersion(self):
        # not a get, not return string
        os.system('uname -r')
    
    def kernelVers(self):
        self.kernelVersion()
        
    def distroVersion(self):
        os.system('lsb_release -a')
    
    def distroVers(self):
        return self.distroVersion()
    
    def kernel(self):
        return self.kernelVers()
    
    def distro(self):
        return self.distroVers()
    
    def command(self,cmd):
        return os.system(cmd)
    
    def cmd(self,cmd):
        return self.command(cmd)
    
