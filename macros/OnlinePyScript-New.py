import onlinepyscript
if 'ONLINE_PY_SCRIPT' not in globals():
    ONLINE_PY_SCRIPT = onlinepyscript.OnlinePyScript(globals())

print 'Creating a new script on collabedit.com ...', 
editUrl = ONLINE_PY_SCRIPT.new()
print 'done'
print 'Your script is available at %s' % editUrl
print 'Remember to change the language to python when visiting this address.'