#!/bin/bash

rm ./gtm/src/main/models/*.xml
mvn clean install

#../deleteDB.sh EventPlatformAG
#../createDB.sh EventPlatformAG

cd /usr/local/actiongui/EventPlatformAG/vm
mvn jetty:run-war
