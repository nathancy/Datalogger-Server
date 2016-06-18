from django import forms
from .models import Logger 

class Loggerform(forms.Form):
    baudrate = forms.IntegerField(label = "Baudrate ", initial = 115200)
    file_name = forms.CharField(label= "File Name ", max_length = 100) 
    update_rate = forms.IntegerField(label ="Update Rate ", initial = 0)
    dataport = forms.CharField(label = "Data Port", max_length = 50, initial = "ttyAMA0")
    timeout = forms.IntegerField(label = "Timeout", initial = 5)

    def clean_baudrate(self):
        if not self['baudrate'].html_name in self.data:
            return self.fields['baudrate'].initial
        return self.cleaned_data['baudrate']

class UploadFileForm(forms.Form):
    filename = forms.CharField(max_length=50)
    docfile = forms.FileField(label = 'Select a file', help_text = '.txt files only')

'''
    def process(self):
        cd = self.cleaned_data
        Logger.objects.create(name = cd.cleaned_data['file_name'])

        '''
