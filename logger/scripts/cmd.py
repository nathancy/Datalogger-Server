import datetime, argparse, time, serial

parser = argparse.ArgumentParser(description = "Datalogger. Baudrate(-b) default:     115200, Update data rate(-r) default: 0 (auto streaming), File name(-n) REQUIRED,     Data port(-p) default: ttyAMA0, Timeout(-t) default: 5")
parser.add_argument('-b', help="Baudrate", default = 115200,required = False)
parser.add_argument('-r', help ="Update rate", default = 0, required= False)
parser.add_argument('-n', help = "Name for file", required = True)
parser.add_argument('-p', help = "Data port", default = "ttyAMA0", required = False)
parser.add_argument('-t', help = "Timeout", default = 5, required = False)
args = vars(parser.parse_args())

class logger(object):
    data_field = None
    def __init__(self, filename = "Data_", baudrate = 115200, interval = 0):
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
        self.data_field.write(str(self.ser.baudrate) + "\n")
        self.data_field.write(str(args['r']) + "\n")
        self.data_field.write(str(args['n']) + "\n")
        self.data_field.write(str(self.ser.port) + "\n")
        self.data_field.write(str(self.ser.timeout) + "\n")
        self.data_field.write("\n")
        
        #print self.ser.baudrate
        #print args['r']
        #print args['n']
        #print self.ser.port
        #print self.ser.timeout
    
    #def __del__(self):
    #    if(self.data_field != None):
    #        self.data_field.close()
    
    def read_data(self):
        time.sleep(self.interval)
        current_time = datetime.datetime.now().strftime("%m_%d_%Y::%H_%M_%S_%f")
        #print current_time[:-3] + "," + self.ser.readline(),
        self.data_field.write(str(current_time[:-3]) + ",")
        self.data_field.write(str(self.ser.readline()))
log = logger()
while True:
    try:
        log.read_data()
    except Exception as e:
        print e
        self.ser.close()
        break
