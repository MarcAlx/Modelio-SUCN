"""
    Created by Marc-Alexandre Blanchard && Enis Kulla

    SUCN - スケン

    export
"""

"""
    The following part of the code came from coExplorer, it's here to avoid the loading of coExplorer by the user
    it's needed to use theUMLFactory
"""
try:
    from org.modelio.api.modelio import Modelio
    orgVersion = True
except:
    orgVersion = False

import os
import sys 

WORKSPACE_DIRECTORY=Modelio.getInstance().getContext().getWorkspacePath().toString()
if orgVersion:
    MACROS_DIRECTORY=os.path.join(WORKSPACE_DIRECTORY,'macros')
else:
    MACROS_DIRECTORY=os.path.join(WORKSPACE_DIRECTORY,'.config','macros')

SCRIPT_LIBRARY_DIRECTORY=os.path.join(MACROS_DIRECTORY,'lib')
sys.path.extend([MACROS_DIRECTORY,SCRIPT_LIBRARY_DIRECTORY])

from misc import *
from modelioscriptor import *
from introspection import *
"""
    end coExplorer import
"""

#lib import
import re

#gui import
from org.eclipse.swt.widgets import Shell
from org.eclipse.jface.dialogs import MessageDialog
from org.eclipse.swt.widgets import FileDialog

class Exporter(object):
    """
        Export a package to .sucn
    """
    __Version,__Name=1.0,"SUCN file exporter to Modelio"

    #used to save element from model
    __actors    = []
    __usecases  = []

    #to store strings that will be saved to file 
    __tosave = []

    def export_package(self,package):
        """
            export selected package to .sucn
        """
        #first retrieve elements
        self.retrieve_actors(package)
        self.retrieve_usecases(package)

        #add actors to __tosave
        self.actors_to_strings()
        #add usecases to __tosave
        self.usecases_to_string()

        #search actors inheritance in order to add them to __tosave
        self.search_actors_inheritance()

        #search communication link between actor and usecase
        self.search_uses()

        #search communication link between usecase and usecase
        self.search_links()

        #search usecase inclusion
        self.search_usecase_inclusion()

        #search usecase extension
        self.search_usecase_extension()

        #save
        self.save_to_file()

    def save_to_file(self):
        """
            save __tosave to file, after prompting to a filename
        """
        fd = FileDialog(Shell(), SWT.SAVE);
        filename = fd.open()
        if(filename!=None):
            #check filename
            if not re.match(".*\.sucn", filename):
                filename+=".sucn"
            #save
            f = open(filename,"w")
            for line in self.__tosave:
                f.write(line+"\n")
            f.close()

    def search_usecase_inclusion(self):
        """
            search usecase inclusions between usecases in order to create -includes- relations
        """
        for usecase in self.__usecases:
            for used in usecase.getUsed():
                for extension in used.getExtension():
                    if (extension.getName() == "include"):
                        self.__tosave.append(used.getOrigin().getName()+' -includes- '+used.getTarget().getName())

    def search_usecase_extension(self):
        """
            search usecase extensions between usecases in order to create -extends- relations
        """
        for usecase in self.__usecases:
            for used in usecase.getUsed():
                for extension in used.getExtension():
                    if (extension.getName() == "extend"):
                        self.__tosave.append(used.getOrigin().getName()+' -extends- '+used.getTarget().getName())

    def search_uses(self):
        """
            search communication links between actors and usescases in order to create -uses- relations
        """
        for actor in self.__actors:
            for end in actor.getOwnedEnd():
                if(isinstance(end.getTarget(),UseCase)):
                    self.__tosave.append(end.getSource().getName()+' -uses- '+end.getTarget().getName())
        self.__tosave.append(" ")

    def search_links(self):
        """
            search for communication links between usecases and usecases to create -islinkedto- relations
        """
        for usecase in self.__usecases:
            for end in usecase.getOwnedEnd():
                if(isinstance(end.getTarget(),UseCase)):
                    self.__tosave.append(end.getSource().getName()+' -islinkedto- '+end.getTarget().getName())
        self.__tosave.append(" ")

    def search_actors_inheritance(self):
        """
            go through __actors then search for actors parents
        """        
        for actor in self.__actors:
            for parent in actor.getParent():
                self.__tosave.append(parent.getSuperType().getName()+" -isparentof- "+actor.getName())
        self.__tosave.append(" ")

    def retrieve_actors(self,package):
        """
            retrieve actors inside package and add them to __actors
        """
        for element in package.getOwnedElement():
            if(isinstance(element,Actor)):
                self.__actors.append(element)

    def retrieve_usecases(self,package):
        """
            retrieve usecase inside package and add them to __usecases
        """
        for element in package.getOwnedElement():
            if(isinstance(element,UseCase)):
                self.__usecases.append(element)

    def actors_to_strings(self):
        """
            convert actors to sucn creation string
        """
        for actor in self.__actors:
            self.__tosave.append("actor "+actor.getName())
        self.__tosave.append(" ")

    def usecases_to_string(self):
        """
            convert actors to sucn creation string
        """
        for usecase in self.__usecases:
            self.__tosave.append("usecase "+usecase.getName())
        self.__tosave.append(" ")

def main():
    """
        called at launch
    """
    e = Exporter()
    if len(selectedElements)!=1 or not isinstance(selectedElements[0],Package):
        MessageDialog.openWarning(Shell(), "Warning", "You must select one package !")
    else:
        e = Exporter()
        e.export_package(selectedElements[0])

#call main
main()