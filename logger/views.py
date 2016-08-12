import os, datetime, subprocess, psutil
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoggerForm, UploadForm 
from .models import Logger, Document
from django.template import RequestContext
from wsgiref.util import FileWrapper
from shutil import make_archive

#Initial variables to hold status of logger
p = None 
logger_alive = False
initial_server_run = True
temp = {"baudrate": " ", "filename": " ", "update_rate": " ", "dataport": " ", "timeout":" "}
status = {"current": "Not Logging"}

#Startpage at 10.0.1.135:8000
def Startpage(request):

    #Collect all logger history 
    post = Logger.objects.all()
    global temp
    global status
    global logger_alive

    #Get current time
    current_time = datetime.datetime.now()

    #If press stop button
    if request.POST.get('stop'):

        #Stop logger, change current status, change current settings
        Kill_logger(p.pid)
        status = {"current": "Not Logging"}
        logger_alive = False
        logger_settings = {"baudrate": " ", "filename": " ", "update_rate": " ", "dataport": " ", "timeout":" "}
        temp = logger_settings

    #Send variables to html page 
    return render(request, 'logger/startpage.html', {'post':post, 'temp':temp, 'status':status})

#New datalogger at 10.0.1.135:8000/logger/CSV_form
def New_form_CSV(request):
    global p
    global logger_alive
    global initial_server_run
    global temp
    global status
   
    #Create form for entering in logger settings 
    form = LoggerForm(request.POST)
    status = {"current": "Not Logging"}
    if initial_server_run is True:
        logger_settings = {"baudrate": " ", "filename": " ", "update_rate": " ", "dataport": " ", "timeout":" "}
        initial_server_run = False
    else:
        logger_settings = temp
    
    #Change status of logger
    if logger_alive is True:
        status = {"current": "Logging"}
    else:
        status = {"current": "Not Logging"}

    #Blank/default logger
    if not form.is_valid() and request.POST.get('submit'):
        
        #Kill previous logger
        if logger_alive is True:
            Kill_logger(p.pid)

        #Create history of logger
        Logger.objects.create(name = "default_logger", baudrate = "115200", update_rate = "0", data_port = "ttyAMA0", timeout = "5") 
   
        #Run background script to start logger
        p = subprocess.Popen(["python", '/home/pi/Documents/Server/Django-server/logger/scripts/log_csv.py', "-n", "default_logger", "-r","0", "-b", "115200", "-p", "ttyAMA0", "-t", "5"])
        status = {"current": "Logging"}
        logger_alive = True
        logger_settings = {"baudrate":"115200", "filename": "default_logger", "update_rate": "0", "dataport":"ttyAMA0", "timeout":"5"}
        temp = logger_settings

    #Logger with user specified settings
    if form.is_valid():    
        if request.POST.get('submit'):
            if logger_alive is True:
                Kill_logger(p.pid)
            clean_baudrate = form.cleaned_data['baudrate']
            clean_name = form.cleaned_data['file_name']
            clean_update_rate = form.cleaned_data['update_rate']
            clean_dataport = form.cleaned_data['dataport']
            clean_timeout = form.cleaned_data['timeout']
    
            #Create history of logger
            Logger.objects.create(name = clean_name, baudrate = clean_baudrate, update_rate = clean_update_rate, data_port = clean_dataport, timeout = clean_timeout) 

            #Start background script
            p = subprocess.Popen(["python", '/home/pi/Documents/Server/Django-server/logger/scripts/log_csv.py', "-n", clean_name, "-r", str(clean_update_rate), "-b", str(clean_baudrate), "-p", str(clean_dataport), "-t", str(clean_timeout)])
            status = {"current": "Logging"}
            logger_alive = True
            logger_settings = {"baudrate":str(clean_baudrate), "filename":clean_name, "update_rate": str(clean_update_rate), "dataport": str(clean_dataport), "timeout": str(clean_timeout)}
            temp = logger_settings

    #If stop button pressed, stop background script
    if request.POST.get('stop'):
        Kill_logger(p.pid)
        status = {"current": "Not Logging"}
        logger_alive = False
        logger_settings = {"baudrate": " ", "filename": " ", "update_rate": " ", "dataport": " ", "timeout":" "}
        temp = logger_settings

    #Send variables to html page
    return render(request, 'logger/new_CSV_logger.html', {'form': form, 'status':status, 'logger_settings':logger_settings})

#Kill background logger script
def Kill_logger(proc_pid):
     process = psutil.Process(proc_pid)
     for proc in process.children(recursive=True):
         proc.kill()
     process.kill()

#Upload files
def Upload_file(request):
    if request.method == 'POST' and request.POST.get('file-upload'):
        fileform = UploadForm(request.POST, request.FILES)
        if fileform.is_valid():
            Handle_uploaded_file(request.FILES['doc_file'])
            return HttpResponseRedirect("")
    else:
        fileform = UploadForm()

    #Create history of uploaded files
    documents = Document.objects.all()
    return render_to_response('logger/upload.html',{'documents': documents, 'fileform':fileform},context_instance=RequestContext(request))

#Copy file onto server
def Handle_uploaded_file(file):
    if file:
        #Replace spaces in filename with "_" otherwise it can't be deleted
        destination = open("/home/pi/Documents/Server/Django-server/logs/" + str(file.name).replace(" ","_"), "wb+")
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

#Display files in media directory
def View_files(request, file_name=""):
    path = "/home/pi/Documents/Server/Django-server/logs/"
    files = os.listdir(path)

    #Download all files in directory (.zip file)
    if request.POST.get('download-all'):
        file_path = "/home/pi/Documents/Server/Django-server/logs/"+file_name
        path_to_zip = make_archive(file_path, "zip", file_path)
        response = HttpResponse(FileWrapper(file(path_to_zip,'rb')), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=Logger_Files'+file_name.replace(" ", "_")+'.zip'
        return response
    
    #Delete single file on webpage
    if request.POST.get('delete-single-csv'):
        for filename in files:
            if request.POST.get(filename) is not None:
                delete_csv_file = subprocess.Popen(["rm", "/home/pi/Documents/Server/Django-server/logs/" + str(filename)])
                stdoutdata, stderrdata = delete_csv_file.communicate()
                files = os.listdir(path)
    return render(request, 'logger/view_files.html', {'files':files})
    
