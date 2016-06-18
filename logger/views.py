from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import Loggerform, UploadFileForm 
from .models import Logger, Upload
from django.core.urlresolvers import reverse
from django.template import RequestContext
import os, argparse, time, datetime, serial, subprocess, sys, psutil, tempfile, zipfile
from django.views.static import serve
from django.utils.encoding import smart_str
from pprint import pprint
from wsgiref.util import FileWrapper

p = None
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

#Enterinin new datalogger
def new_form(request):
    global p
    form = Loggerform(request.POST)
    if form.is_valid():
        if "submit" in form.data:
            #START HEREHEHREHRHEH START HEREH WHEN YOU COME BACK
            clean_baudrate = form.cleaned_data['baudrate']
            #clean_baudrate = form.clean_baudrate()
            clean_name = form.cleaned_data['file_name']
            clean_update_rate = form.cleaned_data['update_rate']
            clean_dataport = form.cleaned_data['dataport']
            clean_timeout = form.cleaned_data['timeout']
            Logger.objects.create(name = clean_name, baudrate = clean_baudrate, update_rate = clean_update_rate, data_port = clean_dataport, timeout = clean_timeout) 
       
            p = subprocess.Popen(["python", '/home/pi/Documents/Server/Django-server/logger/scripts/cmd.py', "-n", clean_name, "-r", str(clean_update_rate), "-b", str(clean_baudrate), "-p", str(clean_dataport), "-t", str(clean_timeout)])
        elif "stop" in form.data:
            kill_logger(p.pid)
    #html="<html><body>%s</body></html>" %clean_dataport
    #return HttpResponse(html)
    return render(request, 'logger/new_logger.html', {'form': form})

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

def view_files(request):
    
    
    path = "/home/pi/Documents/Server/Django-server/logs/"
    files = os.listdir(path)
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
