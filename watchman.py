#!/usr/bin/python
import os, sys, time
from zlib import adler32
from blessings import Terminal
from subprocess import call

class Watchman:

    def watch(self, dir=".", ignoreHidden=True, callbacks=None):        
        oldHashes = {}
        newHashes = {}
        
        defaultCallbacks = {
            "onChange": self.__onChange, 
            "onRemove": self.__onRemove, 
            "onAdd": self.__onAdd
        }
        if(callbacks):
            callbacks = dict(defaultCallbacks.items() + callbacks.items())
        else:
            callbacks = defaultCallbacks
        
        filenames = self.__getFiles(dir, ignoreHidden)
        
        if(len(filenames) > 25000):
            self.mprint("Thats a lot of files bro (" + str(len(filenames)) + ")")
            return
        
        for file in filenames:
            newHashes[file] = self.__getFileHash(file)
            oldHashes[file] = newHashes[file]
        
        self.mprint("Watching [ " + str(len(filenames)) + " ] files for changes.")
        
        while True:
            filenames = self.__getFiles(dir, ignoreHidden)
            
            # Check for file deletions
            if(len(oldHashes.keys()) > len(filenames)):
                filesRemoved = list(set(oldHashes.keys()) - set(filenames))

                for file in filesRemoved:
                    del(oldHashes[file])
                    del(newHashes[file])
                
                if(len(filesRemoved) <= 5):
                    self.mprint("Files " + str(filesRemoved) + " deleted")
                else:
                    self.mprint(str(len(filesRemoved)) + " files deleted")

                callbacks["onRemove"](filesRemoved)
                continue
            
            # Check for file additions
            elif(len(oldHashes.keys()) < len(filenames)):                
                filesAdded = list(set(filenames) - set(oldHashes.keys()))

                for file in filesAdded:
                    oldHashes[file] = self.__getFileHash(file)
                    newHashes[file] = oldHashes[file]
                
                if(len(filesAdded) <= 5):
                    self.mprint("Files " + str(filesAdded) + " added")    
                else:
                    self.mprint(str(len(filesAdded)) + " files added")
                
                callbacks["onAdd"](filesAdded)
                continue
        
            # Check for changes
            for file in filenames:
                try:
                    newHashes[file] = self.__getFileHash(file)
                
                    if(newHashes[file] != oldHashes[file]):
                        oldHashes[file] = newHashes[file]
                        self.mprint("Change detected in [" + file + "]")
                        callbacks["onChange"](file)
                except IOError:
                    continue
                except KeyError:
                    continue
            
            time.sleep(0.5)
                                     
    # Prints pretty colors to the screen                    
    def mprint(self, string):
        t = Terminal()
        timestamp = time.strftime("%H:%M:%S")
        print t.bold + t.white + "[" + t.yellow + "Watchman v1.0" + t.white + "] " + t.normal + t.white + timestamp + " " + t.normal + string
    
    # Triggered when something is changed
    def __onChange(self, file):
        pass
    
    # Triggered when a file is deleted
    def __onRemove(self, files):
        pass
    
    # Triggered when a file is added
    def __onAdd(self, files):
        pass
 
    # Get the files in the specified space
    def __getFiles(self, dir, ignoreHidden):
        filenames = []

        for root, dirs, files in os.walk(dir):
            if(ignoreHidden == True):
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']
            
            for file in files:
                filenames.append(os.path.join(root, file))

        return filenames
    
    # Get a Adler32 hash of specified file
    def __getFileHash(self, filename):
        hash = 0

        with open(filename) as f:
            while True:
                data = f.read(4096*4)

                if not data:
                    break
                else:
                    hash = adler32(data, hash)

            if hash < 0:
                hash += 2**32

        return str(format(hash, 'x')).zfill(8)



    

def execScript(file):
    Watchman().mprint("\tExecuting '.watchman.sh' script")
    retid = call(["bash", ".watchman.sh"])    
    
    if(retid == 0):
        Watchman().mprint("\tScript exited successfully")
    else:
        Watchman().mprint("\tScript exited with status: " + str(retid))

def main():
    directory = "."
    
    if(len(sys.argv) >= 2):
        directory = sys.argv[1]
    
    watchman = Watchman()
    watchman.watch(dir=directory, callbacks={"onChange": execScript})

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(1)
        
