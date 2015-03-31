Modelio-SUCN
==============
Simple UseCase Notation for Modelio
--------------

SUCN - スケン

This code convert SUCN text to usecase in modelio
Documentation used :
- http://modelioscribes.readthedocs.org/en/latest/UseCaseScribe.html
- https://www.modelio.org/documentation/javadoc-3.1/org/modelio/api/model/IUmlModel.html

Usage - Modelio setup
--------------
- Launch Modelio
- File menu -> switch workspace
- Choose 'Modelio-SUCN' folder
- Relaunch Modelio (in order to have access to menu)
- Open UseCases project

Usage - import .sucn file
--------------
- click on import
- a filechooser open 
- choose a file ( a SUCN file )
- the module create a package named 'SUCN Package' in this package
- the module create a use case diagram in order to allow drag n drop of the created elements
- the module parse the file and create the elements

Usage - export .sucn file
--------------
- Create a use case diagram via modelio
- Select the package that contains the diagram
- clic on export

Grammar
--------------
```
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
```

SUCN import testcases
--------------
Some test case are provided as .sucn file :
- actor_creation.scn -> actor creation
- actor_extension.sucn -> actor extension
- actor_usecase_link.sucn -> actor link to a usecase
- comment.sucn -> comment
- test.sucn -> a simple test
- usecase_creation.sucn -> usecase creation
- usecase_extension.sucn -> usecase extends another useace
- usecase_inclusion.sucn -> usecase includes antoher usecase
- usecases_link.sucn -> usecase is link to another usecase

