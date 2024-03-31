#!/bin/bash
find /home/aidan/Documents/tst/ -depth | xargs -n 1 rename -v 's/(.*)\/([^\/]*)/$1\/\L$2/'

