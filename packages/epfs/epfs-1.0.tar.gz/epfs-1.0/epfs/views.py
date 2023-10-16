from django.shortcuts import render,redirect
from django.http import FileResponse,HttpResponse
from django.conf import settings
from .models import Fileupload
from .forms import Fileform
from django.contrib.staticfiles import finders
import random,pyqrcode,os
# Create your views here.

def index(request):
    return render(request,"sharefile.html")

def sharefile(request):
    if request.method == 'POST':
        form = Fileform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj=Fileupload.objects.all().last()
            keytxt=''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(10)])
            obj.keystring=keytxt
            obj.save()
            keystring='https://epfs.eu.pythonanywhere.com/epfs/view/'+keytxt
            qrcode=pyqrcode.create(keystring)
            qrcode.svg(finders.find("qrcode.svg"),scale=8)
            return HttpResponse("<!DOCTYPE htm><html><head><title>epfs file link</title><meta name='viewport' content='width=device-width, initial-scale=1.0' ></head><body><center><h5>{}<h5><img src='/static/qrcode.svg'/></center></body></html>".format(keystring))
    else:
        form = Fileform()
    return render(request, 'sharefile.html', {
        'form': form
    })

def downloadfile(request,link):
    obj=Fileupload.objects.filter(keystring=link)
    filepath=obj.last().Name.path
    return FileResponse(open(filepath,'rb'))

def removeallfile(request,txt):
    if txt=='ea!^433' :
        os.system("rm -rf /home/epfs/upload")
    return redirect('/')



