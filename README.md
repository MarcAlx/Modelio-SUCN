Modelio-SUCN
==============
Simple UseCase Notation for Modelio
--------------

SUCN - スケン

This code convert SUCN text to USE case in modelio
Documentation used :
    - http://modelioscribes.readthedocs.org/en/latest/UseCaseScribe.html
    - https://www.modelio.org/documentation/javadoc-3.1/org/modelio/api/model/IUmlModel.html


Usage
--------------
1 - user click on import
2 - a filechooser open 
3 - user choose a file ( a SUCN file )
4 - the module create a package named 'SUCN Package' in this package
5 - the module create a use case diagram in order to allow drag n drop of the created elements
6 - the module parse the file and create the elements

Grammar
--------------
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