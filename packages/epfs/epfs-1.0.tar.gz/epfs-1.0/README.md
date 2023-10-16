Erscipcard
=========
epfs is a Django sharing file.

Quick start
-----------
1.Add "epfs" to your INSTALLED_APPS in your project setting.py file:
```
INSTALLED_APPS = [
...,
'epfs',
]
```

2.Include the erscipcard URLconf in your project urls.py like this:

```
path('epfs/', include('epfs.urls')),
```

3.Run ``python manage.py makemigrations``(optional) and ``python manage.py migrate``  to create the epfs models.

then run ``python manage.py createsuperuser`` to create personel for login erscipcard page.

4.Visit http://127.0.0.1:8000/epfs/ to share files.

