# SmartUMa
SmartUMa - a platform that brings your University to life at your fingertips

## Project developed for University course "Distributed Systems".

The goal is to have a dashboard accessible over the Internet that displays useful information about our University's parking lot.
This information includes current number of cars parked, number of spots available, statistics, real time sensor information, etc.

To achieve this we've opted for two (simulated) sensors (one for park entry, one for exit).
These sensors send messages via UDP Sockets to a Raspberry Pi 3 B+ that manages a database and provides useful information via an API.
Lastly, the dashboard makes requests to the API and displays information to the end user.

We'll be implementing fail safe measures regarding the database and security measures (authentication/encryption).


## Architectural Model
![alt text](https://github.com/dcx2202/SmartUMa/blob/master/readme_images/modelo_arquitetural.png)


## Physical Model
![alt text](https://github.com/dcx2202/SmartUMa/blob/master/readme_images/modelo_fisico.png)


### Developed by Diogo Cruz, Diogo Nobrega, Francisco Teixeira, Marco Lima
