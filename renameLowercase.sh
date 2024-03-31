#!/bin/bash

find /arma3/steamapps/workshop/content/107410/ -depth | xargs -n 1 rename -v 's/(.*)\/([^\/]*)/$1\/\L$2/'

