from django import forms
from .models import Logger 

#Form for entering in datalogging variables (CSV logger)
class LoggerForm(forms.Form):
    baudrate = forms.IntegerField(label = "Baudrate ", initial = 115200)
    file_name = forms.CharField(label= "File Name ", max_length = 100) 
    update_rate = forms.IntegerField(label ="Update Rate ", initial = 0)
    dataport = forms.CharField(label = "Data Port", max_length = 50, initial = "ttyAMA0")
    timeout = forms.IntegerField(label = "Timeout", initial = 5)

    #Testing for clean values
    def clean_baudrate(self):
        if not self['baudrate'].html_name in self.data:
            return self.fields['baudrate'].initial
        return self.cleaned_data['baudrate']

#Form for uploading files
class UploadForm(forms.Form):
    doc_file = forms.FileField(label = 'Select a file', help_text = "\nNote: Larger files may take longer")
    #help_text = '\nText files(".DOC", ".PAGES", ".TXT") \nData Files(".CSV", ".TAR", ".DAT") \nAudio Files(".MP3", ".WAV") \nVideo Files(".MOV", ".MP4", ".FLV")')

