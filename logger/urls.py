from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns('datalogger.logger.views', 
        url(r'^$', views.startpage),
        url(r'^logger/form/$', views.new_form),
        url(r'^logger/upload/$', views.upload_file),
        url(r'^logger/files/$', views.view_files),
        )

