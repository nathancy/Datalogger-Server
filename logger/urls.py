from django.conf.urls import url, patterns
from . import views


'''
urlpatterns = [
        url(r'^$', views.startpage),
        url(r'^logger/time/$', views.current_datetime),
        url(r'^logger/log/$', views.log),
        url(r'^logger/form/$', views.new_form),
        url(r'^logger/upload/$', views.upload_file),
        url(r'^logger/read/$', views.read_data), 
]
'''

urlpatterns = patterns('datalogger.logger.views', 
        url(r'^$', views.startpage),
        url(r'^logger/time/$', views.current_datetime),
        url(r'^logger/log/$', views.log),
        url(r'^logger/form/$', views.new_form),
        url(r'^logger/upload/$', views.upload_file),
        url(r'^logger/read/$', views.read_data), 
        )

