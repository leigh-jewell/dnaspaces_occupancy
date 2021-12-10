# Cisco DNA Spraces Occupancy Tester
Cisco DNA Spaces Occupancy testing tool.

A small python script to test out  [Cisco DNA Spaces](https://dnaspaces.io). The script creates a web server
using Flask and connects to DNA Spaces Firehose API to receive device count events. It will then show the data in 
a searchable table.

## Getting Started
* Have a look at the Cisco DNA Spaces API over at [DevNet](https://developer.cisco.com/docs/dna-spaces/#!dna-spaces-location-cloud-api).
To get familiar with the APIs available.
* Clone this repository into a directory to get the helper scripts:
```
git clone https://github.com/leigh-jewell/dnaspaces_occupancy.git
```
### Prerequisites

* Install [Python 3.9+](https://www.python.org/downloads/) with the appropriate distribution for your OS.
* Python Pip
```
python3 -m pip install --user --upgrade pip
```


### Partners Appliction Creation

For your script to receive Firehose API events you need to create an application in [Cisco DNA Spaces Partners](https://partners.dnaspaces.io).  
The steps for creating an application are: 
1. Browse to [Cisco DNA Spaces Partners](https://partners.dnaspaces.io) 
2. Create new app
3. For app type select on prem
4. App Center > Complete APP Name, APP Tag line, APP Description, Primary Industry, App Icon
5. App Tile > Complete APP Tile and App Tile Tag line
6. Events > Check the event "Device Count"
7. Create
8. Select App Activation Sandbox > App Center > Select your new App, click Activate button
9. Sign up and continue
10. Accept Permissions
11. Choose locations that you wish to test
12. Generate App Activation token and copy token
13. Paste this token into the local http://127.0.0.1:5000/ once you start python app.py

### Installing

1. Clone the repo
2. cd into the created directpru
3. Create a virtual environment
4. Activte the virtual environment
5. Install required modules into the virtual environment
```
git clone https://github.com/leigh-jewell/dnaspaces_occupancy.git
cd dnaspaces_occupancy
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Running the scrips

To run the application:

```
python app.py
```
This will run a local Flask web server on http://127.0.0.1:5000 which is helpful for testing.
