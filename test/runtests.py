"""Initial test-running script for pysynphot.
 -->> *** You must set PYSYN_CDBS and PYSYN_USERDATA for these tests to run!!
 -->> *** Stdout and Stderr from this script should be piped to a log file.

Warning: PYSYN_USERDATA should not contain any hyphens ('-'). This
directory is used to construct the names of test files. The
synphot syntax parser will interpret them as a minus sign that terminates
the filename, and some tests will then have errors.
"""

import sys, os, time
import testutil
#=====================================================
#           CONFIGURE TESTS HERE
#=====================================================
tlist=['cos_etc_test',
       'cos_fuv_cases',
       'cos_nuv_cases',
       'ui_test',
       'other_etc_test',
       'ticket82',
       'ticket21',
       'spectest',
       'testwrite',
       'ticket86',
       'wavecat_tests'
       ]
#=====================================================

#Doublecheck environment
for symbol in ('PYSYN_CDBS',):  #,'PYSYN_USERDATA'):
    if symbol not in os.environ:
        raise EnvironmentError("%s must be set to run these tests"%symbol)

import numpy
import pyfits
import pysynphot
from pysynphot import etc


#open the summary file
now=time.gmtime()
if os.getenv("hostname") :
    fname=os.getenv("hostname")+".pysyn_summary.log"
else :
    fname='pysyn_summary.log'
fh=open(fname,'w')
fh.write("%s\n"%time.asctime())

#Print some useful version information
fh.write("numpy version: %s\n"%numpy.__version__)
fh.write("pyfits version: %s\n"%pyfits.__version__)
fh.write("Pysynphot version: %s\n"%etc.version(1))

#
#Run the tests
failed=0
summary=[]
for tname in tlist:
    result=testutil.testall(tname)
    fh.write("%s: %s\n"%(tname,str(result)))
    fh.flush()
    if (len(result.errors) > 0) or (len(result.failures) > 0):
        failed=1

#Don't forget the doctests
nfail,ntest=pysynphot._test()
fh.write("__init__ doctests: run=%d failures=%d\n"%(ntest,nfail))
fh.flush()
if nfail>0:
    failed=1

#Clean up & go home
fh.close()
status={0:'passed',1:'failed'}
print "Test suite %s"%status[failed]
sys.exit(failed)

