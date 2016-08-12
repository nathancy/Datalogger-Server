import datetime, argparse, time, serial

#Imitate input and parse from command line, uses default values if no user specific settings given 
parser = argparse.ArgumentParser(description = "Datalogger. Baudrate(-b) default:     115200, Update data rate(-r) default: 0 (auto streaming), File name(-n) REQUIRED,     Data port(-p) default: ttyAMA0, Timeout(-t) default: 5")
parser.add_argument('-b', help="Baudrate", default = 115200,required = False)
parser.add_argument('-r', help ="Update rate", default = 0, required= False)
parser.add_argument('-n', help = "Name for file", required = True)
parser.add_argument('-p', help = "Data port", default = "ttyAMA0", required = False)
parser.add_argument('-t', help = "Timeout", default = 5, required = False)
args = vars(parser.parse_args())

#Script to take user input (or default settings) and output data to CSV file with timestamp 
class csv_logger(object):
    data_field = None
    
    #Open port, create file, and add specified logger settings
    def __init__(self, filename = "Data_", baudrate = 115200, interval = 0):
    
        #Get current time (Month, Day, Year, Hour, Minute, Second, Microsecond)
        time_stamp = datetime.datetime.now().strftime("%m_%d_%Y::%H_%M_%S_%f")
        self.data_field = open("/home/pi/Documents/Server/Django-server/logs/" + filename +time_stamp[:-3]+".csv", "w+")
        self.interval = interval
        self.ser = serial.Serial(
            port = '/dev/' + args['p'],
            baudrate = int(args['b']),
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,     
            bytesize = serial.EIGHTBITS,
            timeout = int(args['t'])
        )

        #Write settings of logger at top of file
        self.data_field.write("Baudrate: " + str(self.ser.baudrate) + "\n")
        self.data_field.write("Update Rate: " + str(args['r']) + "\n")
        self.data_field.write("File Name: " + str(args['n']) + "\n")
        self.data_field.write("Data Port: " + str(self.ser.port) + "\n")
        self.data_field.write("Timeout: " + str(self.ser.timeout) + "\n")
        self.data_field.write("\n")
        
    #Constantly read each line of data with timestamp
    def read_data(self):
        time.sleep(self.interval)
        current_time = datetime.datetime.now().strftime("%m_%d_%Y::%H_%M_%S_%f")
        self.data_field.write(str(current_time[:-3]) + ",")
        self.data_field.write(str(self.ser.readline()))

#Create instance of logger object
log = csv_logger()

while True:
    try:
        #Read the babies in
        log.read_data()
    except Exception as e:
        print e
        self.ser.close()
        break
