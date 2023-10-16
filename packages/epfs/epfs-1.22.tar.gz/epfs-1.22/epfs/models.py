from django.db import models

# Create your models here.

class Fileupload(models.Model):
    keystring = models.CharField(max_length=10, blank=True )
    Name = models.FileField(upload_to='upload/')    
