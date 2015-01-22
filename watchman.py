#!/usr/bin/python
import os, sys, time
from zlib import adler32
from blessings import Terminal

class Watchman:

    def watch(self, dir=".", ignoreHidden=True, callbacks=None):        
        oldHashes = {}
        newHashes = {}
        
        if not callbacks:
            callbacks = {
                "onChange": self.__onChange, 
                "onRemove": self.__onRemove, 
                "onAdd": self.__onAdd
            }
        
        self.__print("Watching for file system changes.")
        
        while True:
            filenames = self.__getFiles(dir, ignoreHidden)
            
            # Check for file deletions
            if(len(oldHashes.keys()) > len(filenames)):
                filesRemoved = list(set(oldHashes.keys()) - set(filenames))

                for file in filesRemoved:
                    del(oldHashes[file])
                    del(newHashes[file])
                    
                callbacks["onRemove"](filesRemoved)
                continue
            
            # Check for file additions
            elif(len(oldHashes.keys()) < len(filenames)):                
                filesAdded = list(set(filenames) - set(oldHashes.keys()))

                for file in filesAdded:
                    oldHashes[file] = self.__getFileHash(file)
                    newHashes[file] = oldHashes[file]
                    
                callbacks["onAdd"](filesAdded)
                continue
        
            # Check for changes
            for file in filenames:
                newHashes[file] = self.__getFileHash(file)
                
                if(newHashes[file] != oldHashes[file]):
                    oldHashes[file] = newHashes[file]
                    callbacks["onChange"](file)
                                    
            time.sleep(0.1) 
    
    def __print(self, string):
        t = Terminal()
        timestamp = time.strftime("%H:%M:%S")
        print t.bold + t.white + "[" + t.yellow + "Watchman v1.0" + t.white + "] " + t.normal + t.white + timestamp + " " + t.normal + string
    
    def __onChange(self, file):
        self.__print("Change detected in [" + file + "]")
        
    def __onRemove(self, files):
        self.__print("Files " + str(files) + " deleted")
        
    def __onAdd(self, files):
        self.__print("Files " + str(files) + " added")
 
    def __getFiles(self, dir, ignoreHidden):
        filenames = []

        for root, dirs, files in os.walk(dir):
            if(ignoreHidden == True):
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



    
def main():
    watchman = Watchman()
    watchman.watch()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(1)