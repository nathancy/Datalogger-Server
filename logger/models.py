from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.files.storage import FileSystemStorage

import argparse, time, serial, datetime
class Logger(models.Model):
    baudrate = models.PositiveIntegerField(default = 115200)
    update_rate = models.PositiveIntegerField(default = 0)
    name = models.CharField(max_length = 50)
    data_port = models.CharField(max_length = 50, default = 'ttyAMA0')
    timeout = models.PositiveIntegerField(default = 5)
    current_time = models.DateTimeField(default = timezone.now)

    def log_date(self):
        self.current_time = timezone.now()
        self.save()
    def __str__(self):
        return self.name

class Upload(models.Model):
    docfile= models.FileField(upload_to = 'documents/%Y/%m/%d')

class serial_port(object):
    data_field = None
    def __init__(self, filename= "Data_", baudrate=115200, interval=.5):
        time_stamp=datetime.datetime.now().strftime("%m_%d_%Y::%H_%M_%S_%f")
        self.data_field=open(filename+time_stamp[:-3]+".txt", "w+")
        self.interval=interval
    def __del__(self):
        if(self.data_field != None):
            self.data_field.close()
    def read_data(self):
        time.sleep(self.interval)
        current_time=datetime.datetime.now().strftime("%m_%d_%Y::%H_%M_%S_%f")
        print current_time[:-3]
        self.data_field.write(str(current_time[:-3]) +"\n")
        '''
    def open_serial(self):
        ser = serial.Serial(
            port = 
 '''
