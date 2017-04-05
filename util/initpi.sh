#!/bin/sh

#_MIT License
#_
#_Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
#_
#_Permission is hereby granted, free of charge, to any person obtaining a copy
#_of this software and associated documentation files (the "Software"), to deal
#_in the Software without restriction, including without limitation the rights
#_to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#_copies of the Software, and to permit persons to whom the Software is
#_furnished to do so, subject to the following conditions:
#_
#_The above copyright notice and this permission notice shall be included in all
#_copies or substantial portions of the Software.
#_
#_THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#_IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#_FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#_AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#_LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#_OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#_SOFTWARE.


# Load some software we need onto a new raspbian system:

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y vim vim-scripts screen lynx links
sudo pip install logdissect
git clone https://github.com/dogoncouch/logshell.git
cd logshell
sudo make
cd ..
git clone https://github.com/dogoncouch/dirutils.git
cd dirutils
sudo make
cd ..
git clone https://github.com/dogoncouch/dev-shortcuts.git
sudo cp dev-shortcuts/gitup.sh /usr/local/bin/gitup
sudo rm -rf logshell dirutils dev-shortcuts
