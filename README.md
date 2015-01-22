# Watchman.py
Watchman is simply a Python script that will watch for changes to files in a specified directory and execute a Python callback when changes, additions, or deletions occur.

## Usage
* Install it on a Linux system by placing the file in the `/bin/` or `/usr/bin/` directory. (You may wish to rename it from `watchman.py` to `watchman`)
* In it's current state; it looks for a file called `.watchman.sh` which it will execute on a file change. This script should be in the directory the command is being launched from.
* Command to use is `watchman`.

## Licence
Released under the **MIT Licence**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Copyright (c) 2015 Patrick Hennessy
