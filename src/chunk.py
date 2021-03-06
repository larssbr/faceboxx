#break a file into chunks and join them back 

import pyminizip
import sys
from zipfile import ZipFile
import shutil
import os

# The compression level passed to pyminizip
compression_level = 9

# Number of bytes per chunk uploaded to Facebook
CHUNK_SIZE = 10000000

# Zips inputFile under password and outputs it to output using pyminizip
def zipcrypt(inputFile, output, password):
   pyminizip.compress(inputFile, output, password, compression_level)
   return

# Uses built-in zipfile library to decrypt the zip and extract the contents to the current dir
def zipdecrypt(inputFile, password):
   zip = ZipFile(inputFile)
   zip.extractall(pwd=password)
   return

# Split the file into smaller chunks
def splitFile(inputFile):
   #read the contents of the file
   f = open(inputFile, 'r')
   data = f.read()
   f.close()
   inputFile = inputFile.split(os.path.sep)[-1]
   #print 'original data len' + str(len(data))
   #os.remove(inputFile[:-4])
   #os.remove(inputFile)

   #create a info.txt file for writing metadata
   i = 0
   j = 0
   os.mkdir(inputFile + 'dir')
   
   if len(data) < CHUNK_SIZE:
	   blockfile = open(inputFile + 'dir/' + inputFile + '0', 'w')
	   blockfile.write(data)
	   i += 1
   else:
	   while (CHUNK_SIZE * i < len(data)):
		  #print str(len(block)) + '\n'
		  #blockfile = open(inputFile + 'dir/' + inputFile + str(i), 'wb')
		  blockfile = open(inputFile + 'dir/' + inputFile + str(i), 'w')
		  blockfile.write(data[CHUNK_SIZE * i:CHUNK_SIZE * (i + 1)])
		  #print 'line 40 blocksize: ' + str(len(''.join(block)))
		  i += 1
		  #print 'line 42: i is ', str(i)
		  blockfile.close()
	   if (CHUNK_SIZE * i + j < len(data)):
		  #print 'overflowed!'
		  blockfile = open(inputFile + 'dir/' + inputFile + str(i), 'w') 
		  #print 'i is ' + str(i) + '\n'
		  #print 'CHUNK_SIZE is ' + str(CHUNK_SIZE)
		  #print 'j is ' + str(j)
		  #print 'len of data is ' + str(len(data))
		  #print 'so what is CHUNK_SIZE * i + j?', str(CHUNK_SIZE*i+j)
		  while (((CHUNK_SIZE * i) + j) < len(data)): 
			 #print 'overflowed a bit\n'
			 blockfile.write(data[CHUNK_SIZE * i + j])
			 j += 1
		  blockfile.close()
	   if (j > 0): i += 1
   infofile = open('info.txt', 'w')
   infofile.write(inputFile + ',' + str(i) + ',' + str(CHUNK_SIZE))
   infofile.close()
   return

#define the function to join the chunks of files into a single file
def joinFiles(fileName, noOfChunks):
   # this function works
   data = []
   for i in range(noOfChunks): # change this to check how many pieces are in the folder
      chunkName = fileName + '/' + fileName[:-3] + str(i)
      curChunk = open(chunkName, 'r')
      data.append(curChunk.read())
      curChunk.close()
   shutil.rmtree(fileName) # delete folder of chunks
   joined = open(fileName, 'w')
   joined.write(''.join(data)) # write joined chunk file
   joined.close()
   return

#splitFile('spim.png')
#joinFiles('spim.png') 

'''
# python chunk.py -e file password
if (len(sys.argv) == 4 and sys.argv[1] == "-e"):
   # make encrypted zip
   zipcrypt(sys.argv[2], sys.argv[2] + '.zip', sys.argv[3])

   # call the file splitting function

   splitFile(sys.argv[2] + '.zip')

elif (len(sys.argv) == 4 and sys.argv[1] == "-d"):
   # python chunk.py -d foldername password
   #call the function to join the splitted files
   f = open('info.txt')
   line = f.readline()
   f.close()
   num = line.split(',')[1]
   #print 'num', num
   joinFiles(sys.argv[2], int(num))
   zipdecrypt(sys.argv[2],  sys.argv[3])
else:
   print 'python chunk.py -e file password'
   print 'python chunk.py -d foldername password'
'''
