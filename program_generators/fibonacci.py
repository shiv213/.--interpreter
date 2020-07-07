# This Python program will create a Fibonacci-Program for the ".:" language.

import os, sys, stat, time

# This is the root relative to which the sample program will be created.
# You must edit this to create the directory somewhere fit for your own
# directory structure; e.g. in /dev/null
BASEDIR = './test'

# ----------- BEGIN HELPER FUNCTIONS -----------------

def SetFileYear(filename,year):   
    t = time.mktime((year, 1, 1, 12, 34, 56, 4, 117, 0))    
    os.utime(filename,(t,t))
    
def CreateIntegerVariable(filename,size):
    file = open(filename,'wb')
    file.write( ('?' * size).encode('utf-8') )
    file.close()
    SetFileYear(filename,1991)

def CreateDirectoryRecursive(directory):
    try:
        os.makedirs(directory)
    except:
        # did I tell you that I hate exceptions ? Because you cannot ignore them
        # (as you can with errors). so DOWN WITH EXCEPTION-BASED ERROR INTERFACES.
        pass

# ----------- END HELPER FUNCTIONS -----------------

print("Creating program logic.")
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','0. =','c'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','0. =','d'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','1.print','b'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','2.=','e'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','2.=','f.b'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','3.=','b'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','3.=','c.a'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','4.+=','a'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','4.+=','e'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','5.+=','c'))
CreateDirectoryRecursive(os.path.join(BASEDIR,'japan.kurt','5.+=','f'))

print("Creating the initial variables.")
CreateIntegerVariable(os.path.join(BASEDIR,'a'),1)
CreateIntegerVariable(os.path.join(BASEDIR,'b'),1)
CreateIntegerVariable(os.path.join(BASEDIR,'c'),0)
CreateIntegerVariable(os.path.join(BASEDIR,'d'),20)
CreateIntegerVariable(os.path.join(BASEDIR,'e'),2)
CreateIntegerVariable(os.path.join(BASEDIR,'f'),1)

print("Done.")