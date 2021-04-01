#!/usr/bin/env python3
#Jonathan Goohs and Ryan Serrato
#Lab 8: Parts 1-3
#CAPT Doherty SY402

#imports
import hashlib 
import os 
import time 
import getopt
import sys

#Collaborations
#MIDN Goohs wrote hashing portion
#MIDN Serrato wrote file exceptions and iterations of initial file parsing
#design
#have a dictionary with the paths as keys and the values as tuples of the hashes and their respective timestamp for being observed

#start source code
ignoreList = ['/dev', '/proc', '/run', '/sys', '/tmp', '/var/lib', '/var/run']

listOfFiles = []
rootdir = "/"

def traverseOS(): 
	for subdir, dirs, files in os.walk(rootdir):    #traverse through the entire file system using os.walk
		for file in files: 
			path = os.path.join(subdir, file)
			if path.startswith('/dev') or path.startswith('/proc') or path.startswith('/run') or path.startswith('/sys') or path.startswith('/tmp') or path.startswith('/var/lib') or path.startswith('/var/run'): 
				continue
			listOfFiles.append(path)
			print(path)    
	return listOfFiles        


def getFileInfo(listOfFiles): 
	fileDict = {}
	for files in listOfFiles:
		try:
			time = os.path.getmtime(files)
			hashf = hashlib.sha256()
			with open(files, "rb") as rf:
				for byte in iter(lambda: rf.read(4096), b""):
					hashf.update(byte)
				print("File content's hash: " + hashf.hexdigest())
			val = [hashf.hexdigest(), time]
			fileDict[files] = val
		except:
			print("Exception occured")
	return fileDict


def printData(dictionary): 
	with open('storedhash.txt', 'w+') as f: 
		for k,v in dictionary.items():
			f.write(f'{k}:{v}\n')

def getData(file): 
	dictionary = {}
	with open(file, "r") as f: 
		for line in f: 
			line = line.split(':')
			key = line[0]
			values = line[1].rstrip().split(',')
			values = [values[0], [values[1]]]
			hashVal = values[0][1:].replace('\'', '')
			timeVal = values[1][0].replace(']', '').replace(' ', '')
			vals = [hashVal, timeVal]
			dictionary[key] = vals
		return dictionary 

def compareData(dict1, dict2): 
	newFiles = {}
	missingFiles = {}
	modifiedFiles = {}
	og_keys = set(dict1.keys())
	new_keys = set(dict2.keys())
	shared_keys = og_keys.intersection(new_keys) 

	removedFiles = og_keys - new_keys
	newFiles = new_keys - og_keys 
	
	for x in shared_keys:
		if dict1[x][0] != dict2[x][0]: 
			modifiedFiles[x] = [dict1[x][0], dict2[x][0]]	

	print(f'New Files Found: {newFiles}\n\n')
	print(f'Removed Files: {removedFiles}\n\n')
	print(f'Modified Files: {modifiedFiles.keys()}')

def usage(): 
	print('***   Python File Integrity Checker     ***')
	print('Usage: sudo ./hash.py [option]\n')
	print('Options: ')
	print('-u --updateScan : Updates the scan of the file system, and alerts you of changed, new, or deleted files by comparing to output of intial scan\n')
	print('-i --initialScan : Runs the intial scan of the file system, storing all files with timestamps and hashes in storedhash.txt\n')
	print('Please run with either -i or -u option. For first run, use -i.')
	exit()

def main():
	try: 
		opts, args = getopt.getopt(sys.argv[1:], "iu", ["initialScan", "updateScan"])
	except getopt.GetoptError as err: 
		print(err)
		usage()
	for o, a in opts: 
		if o in ("-i", "--initialScan"): 
			listOfFiles = traverseOS()
			dictionary = getFileInfo(listOfFiles)
			printData(dictionary)
		elif o in ("-u", "--updateScan"): 
			originalFiles = getData("storedhash.txt")
			listOfFiles = traverseOS()
			dictionary = getFileInfo(listOfFiles)
			compareData(originalFiles, dictionary)
			printData(dictionary)
		else: 
			usage()
	usage()

if __name__ == "__main__":
	main()

#retrieve comparison of initial flags vs. later point flags
#dump things into new list, changed list, deleted list

#os.path.getmtime(file)      #retreives the last modified time 
