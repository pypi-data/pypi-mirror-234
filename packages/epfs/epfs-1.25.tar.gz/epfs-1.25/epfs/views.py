from django.shortcuts import render,redirect
from django.http import FileResponse,HttpResponse
from django.conf import settings
from .models import Fileupload
from .forms import Fileform
#from django.contrib.staticfiles import finders
import random,pyqrcode,os,base64
from zipfile import ZipFile

def index(request):
    return render(request,"epfs/sharefile.html")

def sharefile(request):
    if request.method == 'POST':
        form = Fileform(request.POST, request.FILES)
        files = request.FILES.getlist('Name')
        if form.is_valid():
            #form.save()
            keytxt=''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(10)])
            for f in files:
                file_instance = Fileupload(Name=f,keystring=keytxt)
                file_instance.save()                
            keystring=request.META['HTTP_HOST'] + '/epfs/view/' + keytxt
            qrcode=pyqrcode.create(keystring)
            qrcode.svg("qrcode.svg",scale=8)
            imgfile=base64.b64encode(open("qrcode.svg","rb").read()).decode('ascii')
            return HttpResponse("<!DOCTYPE htm><html><head><title>epfs file link</title><meta name='viewport' content='width=device-width, initial-scale=1.0' ></head><body><center><h5>{}<h5><img src='data:image/svg+xml;base64,{}' /></center></body></html>".format(keystring,imgfile))
    else:
        form = Fileform()
    return render(request, 'epfs/sharefile.html', {
        'form': form
    })

def downloadfile(request,link):
    obj=Fileupload.objects.filter(keystring=link)
    if obj.count() == 1 :
        return FileResponse(open(obj.last().Name.path,'rb'))
    zipobj = ZipFile('download.zip', 'w')
    for i in obj:
        filepath=i.Name.path
        filename=i.Name.name
        zipobj.write(filepath,filename)
    zipobj.close()    
    f=open('download.zip','rb')
    fdown=f.read()
    f.close()
    os.remove('download.zip')
    response = HttpResponse(fdown, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={}.zip'.format(link)
    return response

def removeallfile(request,txt):
    path=os.path.join(settings.BASE_DIR)
    path=os.path.dirname(path)
    path=os.path.join(path,'upload')
    if txt=='ea!^433' :
        os.system("rm -rf {}".format(path))
    return redirect('/epfs')



