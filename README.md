# Inventory Checker
This application is used to check the availability of PS5's at various implemented locations.

This should be run as a docker container.

## Using and Deploying

Step 1:
* To use this container, we to define some user-specific data that is unique to your use-case. All user-specific
  data is stored in `app/config.ini`. You will need to make a copy of `config-example.ini`:
   ```aidl
   cp app/config-example.ini app/config.ini
   ```

  Once done, you can open `config.ini` and enter your own information.

Step 2:
* Build the docker container with your new information. This can be done fairly easily using the `Makefile`
  ```aidl
  # To build the container and launch it:
  make exec
  
  # To build the container only:
  make build
  ```
* (Optionally) You can pass a `path` argument to Make, that will override the location of `config.ini`. By default,
the container will read config.ini from the location within your code repo that you just copied, i.e. 
  `${YOUR FULL PATH}/inventory-check/app/config.ini`. If you use the `path` override, it will read the file 
  from the location you specify. For example
  ```aidl
  make exec path=/Users/testuser1/configs
  ```
  
Step 3:
* Once launched, you will have a docker container that polls at regular intervals (specified in your config.py file)
* To view all logs of the container, use `docker logs -f inventory-check`
* To stop and remove the container, use `docker stop inventory-check`
* To stop and remove the container, use `docker rm -f inventory-check`

## Development
If you would like to develop this app further, please start by installing the dev dependencies in:

`pip3 install -r requirements-dev-txt`

Then edit the application as you see fit. You can test the application by running ```python3 app/main.py```
which will start the polling process of the application and log output to stdin/stdout.