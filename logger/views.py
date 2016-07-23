from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import Loggerform, UploadFileForm, Button_Form
from .models import Logger, Upload, Logger_status
from django.core.urlresolvers import reverse
from django.template import RequestContext
import os, argparse, time, datetime, serial, subprocess, sys, psutil, tempfile, zipfile, shlex
from django.views.static import serve
from django.utils.encoding import smart_str
from pprint import pprint
from wsgiref.util import FileWrapper
from shutil import make_archive

p =None 
alive = False
initial_server_run = True
temp = {"baudrate": " ", "filename": " ", "update_rate": " ", "dataport": " ", "timeout":" "}
status = {"current": "Not Logging"}
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
    global temp
    global status
    global alive
    form = Loggerform(request.POST)
    if "stop" in form.data:
        kill_logger(p.pid)
        status = {"current": "Not Logging"}
        alive = False
        logger_settings = {"baudrate": " ", "filename": " ", "update_rate": " ", "dataport": " ", "timeout":" "}
        temp = logger_settings
    return render(request, 'logger/startpage.html', {'post':post, 'temp':temp, 'status':status})

#Enterinin new datalogger
def new_form(request):
    global p
    global alive
    global initial_server_run
    global temp
    global status
    form = Loggerform(request.POST)
    status = {"current": "Not Logging"}
    if initial_server_run is True:
        logger_settings = {"baudrate": " ", "filename": " ", "update_rate": " ", "dataport": " ", "timeout":" "}
        initial_server_run = False
    else:
        logger_settings = temp
    
    #alive_or_not = subprocess.Popen(["px aux | grep python"])
    #alive_or_not = subprocess.Popen(["ps", "aux", "|", "grep", "python"])
    #alive_or_not = subprocess.Popen(["ps", "aux", "|","grep", "cmd.py", "|", "grep", "-v", "color=auto"])
    #print "alive_or_not value is " + str(alive_or_not)
    
    if alive is True:
        status = {"current": "Logging"}
    else:
        status = {"current": "Not Logging"}

    #Blank/default logger
    if not form.is_valid() and "submit" in form.data:
        #Kill previous logger
        if alive is True:
            kill_logger(p.pid)
        Logger.objects.create(name = "default_logger", baudrate = "115200", update_rate = "0", data_port = "ttyAMA0", timeout = "5") 
   
        p = subprocess.Popen(["python", '/home/pi/Documents/Server/Django-server/logger/scripts/cmd.py', "-n", "default_logger", "-r","0", "-b", "115200", "-p", "ttyAMA0", "-t", "5"])
        status = {"current": "Logging"}
        alive = True
        logger_settings = {"baudrate":"115200", "filename": "default_logger", "update_rate": "0", "dataport":"ttyAMA0", "timeout":"5"}
        temp = logger_settings
    #Logger with fill in form
    if form.is_valid():    
        if "submit" in form.data:
            if alive is True:
                kill_logger(p.pid)
            clean_baudrate = form.cleaned_data['baudrate']
            clean_name = form.cleaned_data['file_name']
            clean_update_rate = form.cleaned_data['update_rate']
            clean_dataport = form.cleaned_data['dataport']
            clean_timeout = form.cleaned_data['timeout']
    
            Logger.objects.create(name = clean_name, baudrate = clean_baudrate, update_rate = clean_update_rate, data_port = clean_dataport, timeout = clean_timeout) 

            p = subprocess.Popen(["python", '/home/pi/Documents/Server/Django-server/logger/scripts/cmd.py', "-n", clean_name, "-r", str(clean_update_rate), "-b", str(clean_baudrate), "-p", str(clean_dataport), "-t", str(clean_timeout)])
            status = {"current": "Logging"}
            alive = True
            logger_settings = {"baudrate":str(clean_baudrate), "filename":clean_name, "update_rate": str(clean_update_rate), "dataport": str(clean_dataport), "timeout": str(clean_timeout)}
            temp = logger_settings

    if "stop" in form.data:
        kill_logger(p.pid)
        status = {"current": "Not Logging"}
        alive = False
        logger_settings = {"baudrate": " ", "filename": " ", "update_rate": " ", "dataport": " ", "timeout":" "}
        temp = logger_settings
    #html="<html><body>%s</body></html>" %clean_dataport
    #return HttpResponse(html)
    return render(request, 'logger/new_logger.html', {'form': form, 'status':status, 'logger_settings':logger_settings})

#Currently logging
def currently_logging(request):
    form = Loggerform(request.POST)
    #if form.is_valid():
       # try:
        #    p.wait(timeout=3)
        #except subprocess.TimeoutExpired:
            #kill_logger(p.pid)
    return render(request, 'logger/currently_logging.html', {'form':form})

#Kill background script
def kill_logger(proc_pid):
     process = psutil.Process(proc_pid)
     for proc in process.children(recursive=True):
         proc.kill()
     process.kill()

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

def view_files(request, file_name=""):
    form = Button_Form(request.POST)
    path = "/home/pi/Documents/Server/Django-server/logs/"
    files = os.listdir(path)
    if "download-all" in form.data:
        file_path = "/home/pi/Documents/Server/Django-server/logs/"+file_name
        path_to_zip = make_archive(file_path, "zip", file_path)
        response = HttpResponse(FileWrapper(file(path_to_zip,'rb')), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=Logger_Files'+file_name.replace(" ", "_")+'.zip'
        return response
    return render(request, 'logger/view_files.html', {'files':files})
    
   
    '''
    filename= "/home/pi/Documents/Server/Django-server/logs/file.csv"
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type = "text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    response['Content-Length'] = os.path.getsize(filename)
    return response
    '''

    #filepath = "/home/pi/Documents/Server/Django-server/logs/"
    #return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

#Success
def success(request):
    html = "<html><body>Hello</body></html>"
    return HttpResponse(html)
#Read
def read_data(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'text.txt')
    open_file = open(file_path)
    return render(request, 'logger/read.html', {'open_file': open_file}) 
