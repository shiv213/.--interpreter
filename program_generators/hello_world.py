# This Python program will create a HelloWorld-Program for the ".:" language.

import os, sys, stat, time

# You can edit this to create the directory somewhere else; e.g. in /dev/null
# BASEDIR = 'Z:\\Hello'
BASEDIR = ''

print('Creating the print instruction.')
try:
    os.makedirs(os.path.join(BASEDIR,"print"))
except:
    # did I tell you that I hate exceptions ? Because you cannot ignore them
    # (as you can with errors). so DOWN WITH EXCEPTION-BASED ERROR INTERFACES.
    pass

print('Creating the "Hello, World" file')
filename = os.path.join(BASEDIR,"print","variable")
file = open(filename,'w')
file.write( "Hello, World" )
file.close()

print('Setting its date to 1992, so that its a string variable')
def SetFileYear(filename,year):   
    t = time.mktime((year, 1, 1, 12, 34, 56, 4, 117, 0))    
    os.utime(filename,(t,t))
    
SetFileYear(filename,1992)