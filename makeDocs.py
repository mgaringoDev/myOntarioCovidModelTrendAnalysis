# Imports
import os
from os import listdir
from os.path import isfile, join
import time, datetime
import re


import shutil

# Functions
def getListOfJupyterNotebooks():
    cwd = os.getcwd()
    src= cwd+'\\notebooks\\'
    onlyFiles = [f for f in listdir(src) if isfile(join(src, f))]
    fileName = []
    for file in onlyFiles:
        fileName.append(file.split('.')[0])
    
    return src, fileName

def getDstLocation():
    cwd = os.getcwd()
    cwdList = cwd.split('\\')[:-2]
    dst = ''
    for d in cwdList:
        dst = dst+d+'\\'
    dst = dst + 'local_projectNotes\\_data\\'
    return dst

def getNotesDstLocation():
    cwd = os.getcwd()
    cwdList = cwd.split('\\')[:-2]
    dst = ''
    for d in cwdList:
        dst = dst+d+'\\'
    dst = dst + 'local_projectNotes\\_posts\\jupyterNotebooks\\'
    return dst

def copyFile(srcLocation,dstLocation,fileName):
    srcFile = srcLocation + fileName + '.ipynb'
    dstFile = dstLocation + fileName + '.json'
    shutil.copy(srcFile, dstFile)

def modificationDate(filename):
    t = os.path.getctime(filename)
    timeCreated = datetime.datetime.fromtimestamp(t)    
    return timeCreated.strftime("%Y-%m-%d-")

def getTags(filename):
    with open(filename,"r") as notebook:
        line = notebook.readline()

        while line:    
            line = notebook.readline()        
            tag = re.findall(r'TAG:{(.*)}',line)
            if (tag!=[]):
                break
    if (tag!=[]):
        tags = tag[0].replace(',',' ')
    else:
        tags = ''
    return tags+' jupyter'

def getDescription(filename):
    with open(filename,"r") as notebook:
        line = notebook.readline()

        while line:    
            line = notebook.readline()        
            desc = re.findall(r'DESCRIPTION:{(.*)}',line)
            if (desc!=[]):
                break
    if(desc!=[]):
        desc = desc[0]
    else:
        desc = 'Need to add description.'
    return desc

def getTitle(filename):
    # regex [A-Z][a-z]* means any string starting  
    # with capital character followed by many  
    # lowercase letters  
    words = re.findall('[A-Z][a-z]*', filename) 

    # Change first letter of each word into lower 
    # case 
    title = ''
    for word in words: 
        word = chr( ord (word[0]) + 32) + word[1:] 
        title = title + ' '+word.capitalize()
    return title

def main():
	srcLocation, fileNames = getListOfJupyterNotebooks()
	dstLocation = getDstLocation()
	notesLocation = getNotesDstLocation()

	for fileName in fileNames:
    
	    # Copy the file
	    copyFile(srcLocation,dstLocation,fileName)
	    
	    srcFile = srcLocation+fileName + '.ipynb'
	    dstFile = dstLocation+fileName + '.json'
	    mdFileName = notesLocation+modificationDate(srcLocation+fileName+'.ipynb')+fileName+'.md'
	    
	    # Create post
	    #open file
	    #get the name (date)
	    #write file
	    with open(mdFileName,'w') as mdFile:
	        mdFile.write('---\n')
	        mdFile.write('layout:     myNotebookTemp\n')
	        mdFile.write(f'title:     {getTitle(fileName)}\n')
	        mdFile.write('author:     Mario Garingo\n')
	        mdFile.write(f'tags:     {getTags(srcFile)}\n')
	        mdFile.write(f'description:     {getDescription(srcFile)}\n')
	        mdFile.write('category:     project1\n')
	        mdFile.write('type:     codes\n')
	        mdFile.write(f'notebookfilename:     {fileName}\n')
	        mdFile.write('---\n')

if __name__ == '__main__':
	main()