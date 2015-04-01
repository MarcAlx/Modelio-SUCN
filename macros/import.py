"""
    Created by Marc-Alexandre Blanchard 

    SUCN - スケン

    Grammar :
        +---------------------Purpose----------------------+--------------------Grammar---------------------+-------Example-------+
        | actor creation                                   | 'actor <actor-name>'                           | actor A1            |
        +--------------------------------------------------+------------------------------------------------+---------------------+
        | actor inheritance                                | '<actorA-name> -isparentof- <actorB-name>'     | A1 -isparentof- A2  |
        +--------------------------------------------------+------------------------------------------------+---------------------+
        | actor uses a usecase        (communication link) | '<actor-name> -uses- <usecase-name>'           | A1 -uses- U2        |
        +--------------------------------------------------+------------------------------------------------+---------------------+
        | usecase linked to a usecase (communication link) | '<usecase-name> -islinkedto- <usecase-name>'   | U1 -islinkedto- U2  |
        +--------------------------------------------------+------------------------------------------------+---------------------+
        | usecase creation                                 | 'usecase <usecase-ame>'                        | usecase U1          |
        +--------------------------------------------------+------------------------------------------------+---------------------+
        | usecase inclusion                                | '<usecase-name> -includes- <usecase-name>'     | U1 -includes- U2    |
        +--------------------------------------------------+------------------------------------------------+---------------------+
        | usecase inheritance                              | '<usecase-name> -extends- <usecase-name>'      | U1 -extends- U2     |
        +--------------------------------------------------+------------------------------------------------+---------------------+
        | comments ((inside code) not processed)           | '--<comment-text>'                             | --a comment         |
        +--------------------------------------------------+------------------------------------------------+---------------------+

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

#GUI import
from org.eclipse.swt.widgets import FileDialog
from org.eclipse.swt.widgets import Text

class FileImporterModule(object):
    """
        Import a SUCN file then translate it
    """
    __Version,__Name=1.0,"SUCN file importer to Modelio"
    __default_transaction_name = "import from SUCN file"

    def __init__(self):
        self.__utils       = Utils(theUMLFactory())

    def init_package(self):
        self.__utils.create_or_clean_base_package()
        self.__res_package = instanceNamed(Package,self.__utils.get_package_name())
        self.__translator  = Translator(theUMLFactory(),self.__res_package)

    def import_SUCN(self):
        """
            import SUCN file then translate
        """
        self.init_package()
        filename = self.askFile()
        if(filename!=None):
            fileContent = self.fileToList(filename)
            self.__utils.create_or_clean_base_package()
            self.__translator.make_translate_transaction(self.__default_transaction_name,fileContent)

    def fileToList(self,path):
        """
            open File at path then add each line to a List
        """
        with open(path, "r") as lines:
            res = []
            for line in lines:
                res.append(line.replace('\n',""))
        return res

    def askFile(self):
        """
            ask for a file return full path or None
        """
        fd = FileDialog(Shell(), SWT.OPEN);
        fd.text="Choose a .sucn file to import"
        fd.filterExtensions=["*.sucn"]
        filename = fd.open()
        return filename

class Utils(object):
    """
        provide utilities
    """

    __package_name         = "SUCN Package"
    __usecase_diagram_name = "<drag and drop> element in this diagram"

    def __init__(self,UMLFactory):
        self.__UML_factory=UMLFactory

    def create_or_clean_base_package(self):
            """
                create or clean the working package
            """
            #begin a transaction
            trans = theSession().createTransaction("cleaning package")
            try:
                create=True
                #grab the project
                for e in self.__UML_factory.getModelRoots():
                    if isinstance(e,Project):
                        #search if package exist in it
                        for element in e.getModel().getOwnedElement():
                            #if package exist delete everything in it
                            if isinstance(element,Package) and element.getName()==self.__package_name:
                                #store element in order to delete them
                                #this loop is odd but a single clean seams to not be enough
                                while(len(element.getOwnedElement())>0):
                                    todel = []
                                    for de in element.getOwnedElement():
                                        todel.append(de) 
                                    #delete element in this loop as the previous one is based on a java iterator
                                    for lmt in todel:
                                        todel.pop().delete()
                                create=False                   
                        #create a package
                        if create:
                            self.__UML_factory.createPackage(self.__package_name,e.getModel())
                            #create use case diagram in order to see how what it produce
                            self.__UML_factory.createUseCaseDiagram(self.__usecase_diagram_name,e.getModel(),None)
                trans.commit()
            except:
                trans.rollback()
                raise

    def get_package_name(self):
        return self.__package_name

class Translator(object):
    """
        this class allow translation of SUCN
    """

    def __init__(self,UMLFactory,res_package):
        self.__UML_factory=UMLFactory
        self.__res_package=res_package
        self.__modelio_factory = ModelioFactory(self.__UML_factory,self.__res_package)

    def make_translate_transaction(self,transaction_name,SUCNAsList):
        """
            create transaction and make the translation inside it
        """
        #clean content before translation
        self.__modelio_factory.clean_content()
        #begin translation
        trans = theSession().createTransaction(transaction_name) 
        try:
            self.__translate(SUCNAsList)
            trans.commit()
        except:
            trans.rollback()
            raise

    def __translate(self,SUCNAsList):
        """
            translate SUCN to Modelio
        """
        for SUCNLine in SUCNAsList:
            #comments check and chack first in order to not process it as SUCN line
            if re.match("--.*", SUCNLine):
                pass
            elif re.match(".*\s+-uses-\s+.*", SUCNLine):
                line_split = re.split("\s+",SUCNLine)
                a1 = self.__modelio_factory.get_actor(line_split[0])
                u2 = self.__modelio_factory.get_usecase(line_split[2])
                self.__modelio_factory.create_communication_link(a1,u2)
            elif re.match(".*\s+-islinkedto-\s+.*", SUCNLine):
                line_split = re.split("\s+",SUCNLine)
                u1 = self.__modelio_factory.get_usecase(line_split[0])
                u2 = self.__modelio_factory.get_usecase(line_split[2])
                self.__modelio_factory.create_communication_link(u1,u2)
            elif re.match(".*\s+-isparentof-\s+.*", SUCNLine):
                line_split = re.split("\s+",SUCNLine)
                a1 = self.__modelio_factory.get_actor(line_split[0])
                a2 = self.__modelio_factory.get_actor(line_split[2])
                self.__modelio_factory.create_extends_dependency_between_actors(a2,a1)
            elif re.match(".*\s+-extends-\s+.*", SUCNLine):
                line_split = re.split("\s+",SUCNLine)
                u1 = self.__modelio_factory.get_usecase(line_split[0])
                u2 = self.__modelio_factory.get_usecase(line_split[2])
                self.__modelio_factory.create_extends_dependency_between_usecases(u1,u2)
            elif re.match(".*\s+-includes-\s+.*", SUCNLine):
                line_split = re.split("\s+",SUCNLine)
                u1 = self.__modelio_factory.get_usecase(line_split[0])
                u2 = self.__modelio_factory.get_usecase(line_split[2])
                self.__modelio_factory.create_includes_dependency_between_usecases(u1,u2)
            elif re.match("usecase\s+.*", SUCNLine):
                usecase_name = re.split("\s+",SUCNLine)[1]
                self.__modelio_factory.get_usecase(usecase_name)
            elif re.match("actor\s+.*", SUCNLine):
                actor_name = re.split("\s+",SUCNLine)[1]
                self.__modelio_factory.get_actor(actor_name)

class ModelioFactory(object):
    """ 
        A high level abstraction to modelio
    """
    __actors       = {}
    __usecases     = {}

    def __init__(self,UMLFactory,res_package):
        self.__UML_factory=UMLFactory
        self.__res_package=res_package

    def get_actor(self,name):
        """
            create an actor with name or use an existing one
        """
        if not self.__actors.has_key(name):
            self.__actors[name] = self.__UML_factory.createActor(name,self.__res_package)
        return self.__actors[name]

    def get_usecase(self,name):
        """
            create an actor with name or use an existing one
        """
        if not self.__usecases.has_key(name):
            self.__usecases[name] = self.__UML_factory.createUseCase(name,self.__res_package)
        return self.__usecases[name]

    def create_includes_dependency_between_usecases(self,usecase1,usecase2):
        """
            create an include dependency between usecase1 and usecase2
        """
        return self.__UML_factory.createIncludeUseCaseDependency(usecase1,usecase2)

    def create_extends_dependency_between_usecases(self,usecase1,usecase2):
        """
            create an extends dependency between usecase1 and usecase2
        """
        return self.__UML_factory.createExtendUseCaseDependency(usecase1,usecase2)

    def create_extends_dependency_between_actors(self,actor1,actor2):
        """
            create an extends dependency between actor1 and actor2
        """
        return self.__UML_factory.createGeneralization(actor1,actor2)

    def create_communication_link(self,entity1,entity2):
        """
            create a communication link between two entity which could be actor or usecase
        """
        associationEnd = self.__UML_factory.createAssociationEnd()
        associationEnd.setSource(entity1)
        associationEnd.setTarget(entity2)
        associationEnd.setAssociation(self.__UML_factory.createAssociation())
        associationEnd2 = self.__UML_factory.createAssociationEnd()
        associationEnd2.setSource(entity2)
        associationEnd2.setTarget(entity1)
        associationEnd2.setAssociation(self.__UML_factory.createAssociation())
        
        associationEnd.setOppositeOwner(associationEnd2)
        associationEnd2.setOppositeOwner(associationEnd)
        return associationEnd

    def clean_content(self):
        self.__actors   = {}
        self.__usecases = {}

class MainWindow(object):

    __TITLE = "SUCN translator"
    __WINDOW_SIZE = (250,450)
    __OPACITY = 240

    def __init__(self):
        self.__utils       = Utils(theUMLFactory())
        self.__utils.create_or_clean_base_package()
        self.__res_package = instanceNamed(Package,self.__utils.get_package_name())
        self.__tr = Translator(theUMLFactory(),self.__res_package)
        self.__fi = FileImporterModule()
        self.build_GUI()
        
    def build_GUI(self):
        """
            build main window UI
        """
        self.shell = Shell(SWT.CLOSE)
        self.shell.size = self.__WINDOW_SIZE
        self.shell.minimumSize = self.__WINDOW_SIZE
        self.shell.setLayout (None)
        self.shell.text=self.__TITLE
        self.shell.alpha=self.__OPACITY

        self.button_import = Button(self.shell,SWT.PUSH,text="import .sucn file",widgetSelected = self.on_import_click)
        self.button_import.location = (10,5)
        self.button_import.size = (230,40)
        
        self.label = Label(self.shell,SWT.SINGLE)
        self.label.text="Enter SUCN text here :"
        self.label.location=(10,50)
        self.label.size=(230,30)

        self.input = Text(self.shell,SWT.MULTI)
        self.input.location=(10,70)
        self.input.size=(230,300)
        self.input.text="--add SUCN instruction bellow\n--one instruction by line"
        
        self.button_translate = Button(self.shell,SWT.PUSH,text="Translate",widgetSelected = self.on_translate_click)
        self.button_translate.location = (10,380)
        self.button_translate.size = (115,40)

        self.button_save = Button(self.shell,SWT.PUSH,text="Save as .sucn",widgetSelected = self.on_save_click)
        self.button_save.location = (124,380)
        self.button_save.size = (115,40)

        self.shell.open()

    def on_translate_click(self,event):
        """
            called on translate button click
        """
        input_lines = re.split("\n+",self.input.text)
        self.__utils.create_or_clean_base_package()
        self.__tr.make_translate_transaction("import from SUCN user input",input_lines)

    def on_save_click(self,event):
        """
            called on save button click
        """
        fd = FileDialog(Shell(), SWT.SAVE);
        filename = fd.open()
        if(filename!=None):
            #check filename
            if not re.match(".*\.sucn", filename):
                filename+=".sucn"
            #save
            f = open(filename,"w")
            input_lines = re.split("\n+",self.input.text)
            for line in input_lines:
                f.write(line+"\n")
            f.close()
    
    def on_import_click(self,event):
        """
            called on import button click
        """
        self.__fi.import_SUCN()    

"""
    launching of the module
"""
m = MainWindow()