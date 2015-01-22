#!/usr/bin/python
import os
import time
from zlib import adler32

class FileWatcher:

    def watch(self, dir=".", callback=None):        
        oldHashes = {}
        newHashes = {}
        
        if not callback:
            callback = self.__defaultCallback
        
        print "Listening for file system changes..."
        
        while True:
            filenames = self.__getFiles(dir)
                        
            for file in filenames:
                if(oldHashes.get(file) == None):
                    oldHashes[file] = self.__getFileHash(file)
                    newHashes[file] = oldHashes[file]
                    continue
                    
                newHashes[file] = self.__getFileHash(file)
                
                if(newHashes[file] != oldHashes[file]):
                    oldHashes[file] = newHashes[file]
                    callback(file)
                                    
            time.sleep(0.5) 
        
    def __defaultCallback(self, string):
        print "Change detected in [" + string + "]" 
 
    def __getFiles(self, dir):
        filenames = []

        for root, dirs, files in os.walk(dir):
            for file in files:
                filenames.append(os.path.join(root, file))

        return filenames
    
    def __getFileHash(self, filename):
        hash = 0

        with open(filename) as f:
            while True:
                data = f.read(2048)

                if not data:
                    break
                else:
                    hash = adler32(data, hash)

            if hash < 0:
                hash += 2**32

        return str(format(hash, 'x')).zfill(8)


def cb(string):
    print "Change detected in [" + string + "]" 

watcher = FileWatcher()
watcher.watch()









