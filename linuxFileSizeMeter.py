import os
import pathlib
import sys
import subprocess

class minHeap:
    pass       
def checkFolderSizes(paths): #takes in folder paths and returns size of folders in \
                          # an array [GBStr MBStr KBStr GB MB KB B]
    folderSizes = []
    for path in paths:
        #runs du -b for all paths listed 
        #du -b returns directory size in bytes when run as a command in Linux
        process = subprocess.Popen(["du","-sb",path],stdout=subprocess.PIPE,universal_newlines=True)
        stdout, stderr = process.communicate()
        stdout = stdout.split()
        folderSize = int(stdout[0])
        folderSizeByUnits = formatFolderSize(folderSize)
        folderSizes.append(folderSizeByUnits)
    return folderSizes

def formatFolderSize(folderSizeinBytes): #formats folder size into GB, MB, KB and B/
                                         #All folder size data are equivalent just formated differently
                                         #eg [1GB, 1024MB, 1048576KB, 1073741824B ]
    folderSizeUnits = []
    gigaBytes = folderSizeinBytes/(1024**3)
    megaBytes = folderSizeinBytes/(1024**2)
    kiloBytes = folderSizeinBytes/1024
    folderSizeUnits+=[gigaBytes,megaBytes,kiloBytes,folderSizeinBytes]
    return folderSizeUnits

def printLargestFileUnit(folderSizeByUnits):  #Prints in a unit value bigger than 1
                                              #100MB output instead of .1GB
    if folderSizeByUnits[0]>1:
        return '{:.2f}'.format(folderSizeByUnits[0]).rjust(8) + " GB"
    elif folderSizeByUnits[1]>1:
        return '{:.2f}'.format(folderSizeByUnits[1]).rjust(8) + " MB"
    else:
        return '{:.2f}'.format(folderSizeByUnits[2]).rjust(8) + " KB"

def printOnLoop(paths,lastVal):
    folderSizes = checkFolderSizes(paths)
    if (lastVal!=[]):#formatting data for terminal
        header = 'File Name'.ljust(60) + "Change in File Size".ljust(20) + "\n"
    else:
        header = 'File Name'.ljust(60) + "Starting File Size".ljust(20) + "\n"
    output = ''
    for i in range(len(paths)):
        folderSize = folderSizes[i]
        if (lastVal!=[]): #if this isn't the first loop print changes in folder
            fileSizeChange = folderSize[3]-lastVal[i][3]
            if (fileSizeChange!=0):
                output+= paths[i].ljust(60) + \
                    printLargestFileUnit(formatFolderSize(fileSizeChange/2)) +"/s\n"
        else: #if this is the first loop just print the initial size
            output+= paths[i].ljust(60) + printLargestFileUnit(folderSize) +"\n"
    if (output ==''):
        output+= 'No files have changed size'                
    print(header+output)
    return folderSizes

def main():
    paths = sys.argv[1:]
    timer = 2.0 #by default du called every 2 seconds change here if desired
    lastVal = []
    while(True):
        lastVal = printOnLoop(paths,lastVal)
        # file = open('dummyfile.txt','a')
        # file.write("""Writing dummy text file to test detection of file size changes""")
        file.close()
        time.sleep(timer)

main()
