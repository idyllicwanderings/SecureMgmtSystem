## Running the project

To run a server with a Flask application for the first time type:

  docker-compose up --build

If you visit http://127.0.0.1:5000 you can see your application running. To stop the server use
docker-compose down. You can omit the --build flag next time you want to run the server.

Refer to the Flask tutorials for more information.


## Testing the project

The Flask application comes with some basic tests written using pytest.
Assuming you have pytest installed, invoke:

  pytest

in the project folder to run the tests and see the their results.

