# Datalogger Webserver
A portable datalogger webserver capable of running on any local connection. Includes Python scripts to timestamp and log GPS data (or any data stream via UART) on a Raspberry Pi into .csv files. Implemented using HTML5/CSS web interface to create, edit, remove, or view logging data history.

# Datalogger Features
- Ability to create new logger with specified and standard/default settings. Choose baudrate, desired .csv file name, data stream update rate, port, and timeout.
- File hosting capability.
- View, download, or delete individual files.
- Current logging status with ability to stop logger.

# Developers Guide
In the "Logging History" tab, to show past loggers admin credentials are: 

Username: `admin` 

Password: `spectrum`

To start the server:
Go to directory with the "manage.py" inside. Enter:
```
python manage.py runserver 0.0.0.0:8000
```
To access, go to "IPv4 address:8000" on any web browser.
For example: IPv4 address = 192.168.200.76. Thus run "192.168.200.76:8000" in address bar.

To check if logger is alive:
```
ps aux | grep "python"
```

To check real-time datastream:
```
tail -f "manage.py"
```

