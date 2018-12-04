# SmartUMa
SmartUMa - a platform that brings your University to life at your fingertips
## http://smartumaparking.x10host.com/

## Project developed for University course "Distributed Systems".

The goal is to have a dashboard accessible over the Internet that displays useful information about our University's parking lot.
This information includes current number of cars parked, number of spots available, statistics, real time sensor information, etc.

To achieve this we've opted for two (simulated) sensors (one for park entry, one for exit).
These sensors send messages via UDP Sockets to a Raspberry Pi 3 B+ that manages a database and provides useful information via an API.
Lastly, the dashboard makes requests to the API and displays information to the end user.

We'll be implementing fail safe measures regarding the database and security measures (authentication/encryption).

## Dashboard
### http://smartumaparking.x10host.com/
![alt text](https://github.com/dcx2202/SmartUMa/blob/master/readme_images/dashboard.png)
The dashboard displays the most important information at the top.
Below that there is a graph displaying the number of cars that were parked at each hour today.
At the bottom there is an activity log with a description and time for the most recent events. Next to it are some statistics.


# API
An API serves data related to the parking lot. This data is used by the dashboard to update the displayed information in realtime.
It is possible to get the number of cars parked, the number of free spaces, statistics and many more. For a complete list and paths to get this data please visit:

### http://84.23.208.186:25000/api_help


## Architectural Model
![alt text](https://github.com/dcx2202/SmartUMa/blob/master/readme_images/modelo_arquitetural.png)


## Physical Model
![alt text](https://github.com/dcx2202/SmartUMa/blob/master/readme_images/modelo_fisico.png)


### Developed by Diogo Cruz, Diogo Nobrega, Francisco Teixeira, Marco Lima
