#!/usr/bin/env python

import time, os, sys

def writetofile(filename,mysizeMB):
	# writes string to specified file repeatdely, until mysizeMB is reached. Then deletes fle 
	mystring = "The quick brown fox jumps over the lazy dog"
	writeloops = int(1000000*mysizeMB/len(mystring))
	try:
		f = open(filename, 'w')
	except:
		# no better idea than:
		raise
	for x in range(0, writeloops):
		f.write(mystring)
	f.close()
	os.remove(filename)

############## 

def diskspeedmeasure(dirname):
	# returns writing speed to dirname in MB/s
	# method: keep writing a file, until 0.5 seconds is passed. Then divide bytes written by time passed
	filesize = 1	# in MB
	maxtime = 0.5 	# in sec
	filename = os.path.join(dirname,'outputTESTING.txt')
	start = time.time()
	loopcounter = 0
	while True:
		try:
			writetofile(filename, filesize)
		except:
			# I have no better idea than:
			raise	
		loopcounter += 1
		diff = time.time() - start
		if diff > maxtime: break
	return (loopcounter*filesize)/diff

############## Start of main


def speedTest(dirname):

    print "Let's go"
    print(dirname)
    print 'debug'
	#dirname = sys.argv[1]
    if not os.path.isdir(dirname): 
        return "Specified argument is not a directory. Bailing out"
        #sys.exit(1)


    try:
	speed = diskspeedmeasure(dirname)
	print "Disk writing speed: %.2f Mbytes per second" % speed
    except IOError, e:
		#print "IOError:", e
	if e.errno == 13:
	    print "Could not create test file. Check that you have write rights to directory", dirname
	    speed = -1
    except:
	    print "Something else went wrong"
	    speed = -1
	    raise
    print "done"
    return speed
