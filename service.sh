#!/bin/bash

if [ "$RUN_SERVICE" = false ] ; then
  tail -f /dev/null
  exit
fi

python3 /app/frontend.py -j $WORKERS -p $SLEEP
