# Pepper IoT
This project is developed using [Python 3.9](https://www.python.org/downloads), [MySQL 8](https://www.mysql.com/downloads/) and [Choregraphe Suite](https://developer.softbankrobotics.com/pepper-2-5/downloads/pepper-naoqi-25-downloads-windows)

Upgrade pip via `python -m pip install --upgrade pip`

## Server

### Required Python packages
- **Flask**
```
pip install flask
```
- **DotEnv**
```
pip install python-dotenv
```
- **MySQL Connector**
```
pip install mysql-connector-python
```

- **CORS**
```
pip install flask-cors
```

### Environement settings
Creates an `.env` file in root directory with the following content. Replaces values according to your preferences and machine settings
```
SERVER_PORT=5000
DEBUG_MODE=true

DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_NAME=databasename
```

### Run
1. Launch your MySQL (or equivalent) server
2. Launch [main](server/main.py)

## Raspberry

### Required Python packages
- **Requests**
```
pip install requests
```

### Setup
Choose server IP address and assigned room launching [setup](raspberry/setup.py). It creates a JSON file named settings.cfg with the configuration. If this file already exists you can skip this step: it means that the Raspberry is already configured. If you want to change the configuration you may launch [setup](raspberry/setup.py) again

### Run
1. Launch server application
2. Launch [sensor_manager](raspberry/sensor_manager.py)
