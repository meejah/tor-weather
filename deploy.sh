#!/bin/bash

## This is more-or-less just to write down the sanity-checks needed by
## the Vagrant changes introduced. Eventually, this should grow into a
## one-stop script to deploy a new weather instance.

if [ `cat weather/config/auth_token` == "password" ]; then
   echo "Change auth_token; 'password' is a bad password.";
   exit 3
fi

grep -q "EMAIL_BACKEND" weather/settings.py
if [ $? -eq 0 ]; then
    echo "EMAIL_BACKEND is still in weather/settings.py"
    exit 4
fi

grep -q "weather.dev" weather/config/config.py
if [ $? -eq 0 ]; then
    echo "weather.dev is still in weather/config/config.py"
    exit 5
fi
