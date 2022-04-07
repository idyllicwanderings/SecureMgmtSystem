# README

This is a dockerized version of the ActionGUI framework. It contains two images, a MySQL database and a lightweight linux machine with maven 3.5 and Java 8 installed. To start make sure you have docker installed and type:

`docker-compose up --build`

to build the images and run the containers the first time you use them. Note: If you are using an Apple M1 chip please see `<project_name>/Dockerfile` and change the first import to specify the arm64 architecture.

Once the images have been built you can start and stop the containers using:

`docker-compose up`

and

`docker-compose stop`


## Compiling the project

Once the containers are running (you can check this with `docker ps`  and you should see a 
mysql5 container and a container named `actiongui-app`) you can open a shell inside the 
maven container using:

`docker exec -it actiongui-app bash`

The directory `/usr/local/actiongui/` in the container is linked to the current 
local folder. Anything you create in this folder 
will be visible on your host machine (and vice-versa). Navigate the to the 
folder

    cd /usr/local/actiongui


To compile the code go to the project folder in the container 
and execute maven:

    cd /usr/local/actiongui/EventPlatformAG
    mvn clean install


Next, to create the database, inside the container copy the 
`createDB.sh` script to the directory above and execute it:

    ./createDB.sh EventPlatformAG


## Running the project

Finally, to execute the compiled web application, go to the `EventPlatformAG/vm` directory:

    cd /usr/local/actiongui/EventPlatformAG/vm
    mvn jetty:run-war

The app should be reachable from your local machine under `localhost:8080/vm`. 


## Recompiling the project

If some of the .gtm files changes, delete the corresponsing xml files in the same directory. 
Otherwise, you can delete all of them (assuming you are in the project folder):

    rm ./gtm/src/main/models/*.xml

Compile the project again 

    mvn clean install

If the data model changed, you need to recreate the database. First drop the current database:

    ./deleteDB.sh EventPlatformAG

then create the database again with 

    ./createDB.sh EventPlatformAG


Refer to the ActionGUI tutorial for more information.


## Testing the project

The .gtm files containing "evaluation" in their name have some written test cases.
To execute the tests, run the application and click on the "Evaluation" button.

A menu will appear with buttons that invoke tests for different roles. Before clicking
any of those buttons make sure you click on the first button to clear the database and
set it in an expected state. Otherwise, you may have unexpected errors.
The first button must also be clicked between different tests, as tests themselves may
change the database state. 
