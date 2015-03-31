import encodings
import urllib2
import urllib
import cookielib
import os
import re
import webbrowser

COLLAB_HOST = 'http://collabedit.com/'
COLLAB_NEW = 'http://collabedit.com/new'
COLLAB_GET = 'http://collabedit.com/download?id=%s'
COLLAB_EDIT = 'http://collabedit.com/%s'

class OnlinePyScript(object):
    def __init__(self, executionScope, url=None, editUrl=None ):
        self.url = url
        self.editUrl = editUrl
        self.executionScope = executionScope
        self.cookieJar = cookielib.CookieJar()
        self.webOpener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookieJar))

        
    def set(self, collabIdOrAnyURL, editUrl=None):
        (url,edit_url) = self._computeURL(collabIdOrAnyURL, editUrl)
        try:
            self.webOpener.open(url)
            # urllib2.urlopen(url).read()
        except:
            print 'ERROR: cannot read script at %s' % url
            raise
        self.url = url
        self.editUrl = edit_url
        
        
    def new(self):
        try:
            newurl = self.webOpener.open(COLLAB_NEW).geturl()
            document_id = re.match(COLLAB_HOST+r'(?P<id>\w+)',newurl).group('id')
            (url,edit_url) = self._computeURL(document_id)
            self.url = url
            self.editUrl = edit_url
            return newurl
        except:
            print 'ERROR: Cannot get the reference to a new document '
            raise

            
    def edit(self):
        if self._ifURLIsDefined():
            if self.editUrl is None:
                print 'No url defined for editing the script'
            else: 
                webbrowser.open(self.editUrl)
    
    def run(self):
        if self._ifURLIsDefined():
            script = self.webOpener.open(self.url).read()
            #script = urllib2.urlopen(self.url).read()
            print '---- Executing %s ------' % self.url
            # print script
            exec script in self.executionScope

    
    #----------------------------------------------------------
    #   Class implementation
    #----------------------------------------------------------
    
    def _computeURL(self, collabIdOrAnyURL, editUrl=None):
        if collabIdOrAnyURL.startswith(COLLAB_HOST):
            collab_id = re.match(
                COLLAB_HOST+r'(?P<id>\w+)',collabIdOrAnyURL).group('id')
            return (COLLAB_GET % collab_id, 
                    COLLAB_EDIT % collab_id)
        elif collabIdOrAnyURL.startswith('http'):
            return (collabIdOrAnyURL, editUrl)
        else:
            return (COLLAB_GET % collabIdOrAnyURL, 
                    COLLAB_EDIT % collabIdOrAnyURL)
    
    
    def _ifURLIsDefined(self):
        if self.url is None:
            print 'No online document has been defined.'
            print 'You can either create a new document'
            print 'with the button  "Online > New" or if you'
            print 'the document already exist you can type'
            print 'OnlinePyScript.set("<url>") in the'
            print 'python console'
            return False
        return True

    def getSettingsFile():
        return os.path.join(
            os.path.expanduser('~'),
            '.modelio',
            'pymodelio',
            'settings.py')

    # execfile(settings_file)
