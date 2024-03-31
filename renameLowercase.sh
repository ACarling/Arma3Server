#!/bin/bash

find /arma3/steamapps/workshop/content/107410/ -depth | xargs -n 1 rename -v 's/(.*)\/([^\/]*)/$1\/\L$2/'
find /arma3/steamapps/workshop/downloads/107410/ -depth | xargs -n 1 rename -v 's/(.*)\/([^\/]*)/$1\/\L$2/'

