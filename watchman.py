#!/usr/bin/python
import os
import time
from zlib import adler32

class FileWatcher:

    def watch(self, dir=".", callbacks=None):        
        oldHashes = {}
        newHashes = {}
        
        if not callbacks:
            callbacks = {"onChange": self.__onChange, "onRemove": self.__onRemove, "onAdd": self.__onAdd}
        
        print "Listening for file system changes..."
        
        while True:
            filenames = self.__getFiles(dir)
        
            if(len(oldHashes.keys()) > len(filenames)):
                filesRemoved = list(set(oldHashes.keys()) - set(filenames))

                for file in filesRemoved:
                    del(oldHashes[file])
                    del(newHashes[file])
                    
                callbacks["onRemove"](filesRemoved)
                 
            elif(len(oldHashes.keys()) < len(filenames)):                
                filesAdded = list(set(filenames) - set(oldHashes.keys()))

                for file in filesAdded:
                    oldHashes[file] = self.__getFileHash(file)
                    newHashes[file] = oldHashes[file]
                    
                callbacks["onAdd"](filesAdded)
        
            for file in filenames:
                
                newHashes[file] = self.__getFileHash(file)
                
                if(newHashes[file] != oldHashes[file]):
                    oldHashes[file] = newHashes[file]
                    callbacks["onChange"](file)
                                    
            time.sleep(0.5) 
        
    def __onChange(self, string):
        print "Change detected in [" + string + "]" 
        
    def __onRemove(self, files):
        print "Files deleted"
        
    def __onAdd(self, files):
        print "Files added" 
 
    def __getFiles(self, dir):
        filenames = []

        for root, dirs, files in os.walk(dir):
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            
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









