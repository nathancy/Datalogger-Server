from django.conf.urls import url, patterns
from . import views

#Names for URL in web browser
urlpatterns = [
        url(r'^$', views.Startpage),
        url(r'^logger/CSV_form/$', views.New_form_CSV),
        url(r'^logger/upload/$', views.Upload_file),
        url(r'^logger/files/$', views.View_files),
]

