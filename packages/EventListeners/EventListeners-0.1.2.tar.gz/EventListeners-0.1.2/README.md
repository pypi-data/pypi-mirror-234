# Event Listeners
## Overview
Event listeners are a way to listen for events that occur. They are used to trigger actions when certain events occur. 
For example, you can use an event listener to trigger an action when an event arrives to Event Hub.

## Prerequisites
All required modules are defined in setup.py file. Install all required modules mentioned in *install_requires* section.

## How to run
### Event Hub Listener
Run Listener.py file to listen for events from Event Hub. This listener expects a json file as runtime argument.
A sample json file called config_DEV.json is provided in the repository. This file contains all the required parameters.

Depending on the environment, you can create a json file and pass it as runtime argument to Listener.py file.

