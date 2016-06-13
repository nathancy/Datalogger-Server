from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import Loggerform, UploadFileForm 
from .models import Logger, Upload
from django.core.urlresolvers import reverse
from django.template import RequestContext
import os, argparse, time, datetime, serial

#Log
def log(request):
    post = Logger.objects.all()
    return render(request, 'logger/log.html', {'post':post})
#Time
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>The current time is %s.</body></html>" % now
    return HttpResponse(html)

#Startpage
def startpage(request):
    post = Logger.objects.all()
    return render(request, 'logger/startpage.html', {'post':post})

#Entering in new datalogger
def new_form(request):
    form = Loggerform(request.POST)
    if form.is_valid():
        clean_baudrate = form.cleaned_data['baudrate']
        clean_name = form.cleaned_data['file_name']
        clean_update_rate = form.cleaned_data['update_rate']
        clean_dataport = form.cleaned_data['dataport']
        clean_timeout = form.cleaned_data['timeout']
        Logger.objects.create(name = clean_name, baudrate = clean_baudrate, update_rate = clean_update_rate, data_port = clean_dataport, timeout = clean_timeout) 

        ser = serial.Serial(
            port = '/dev/' + clean_dataport,
            baudrate = clean_baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=clean_timeout
            )
        '''
        while True:
            try: 
                x = ser.readline()
                print x
        '''
    return render(request, 'logger/retrieve.html', {'form': form})

#Upload
def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        newdoc = Upload(docfile = request.FILES['docfile'])
        newdoc.save()
        return HttpResponseRedirect(reverse('datalogger.logger.views.upload_file'))
    else:
        form = UploadFileForm()
    documents = Upload.objects.all()
   
    #return render(request, 'logger/upload.html', {'documents': documents, 'form': form})
    return render_to_response('logger/upload.html',{'documents':documents, 'form':form}, context_instance=RequestContext(request)) 

#Read
def read_data(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'text.txt')
    open_file = open(file_path)
    return render(request, 'logger/read.html', {'open_file': open_file}) 
