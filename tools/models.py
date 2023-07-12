from django.db import models
from django.utils import timezone


class UploadImage(models.Model):
    # process_id = models.CharField(max_length=200)
    image = models.ImageField(upload_to='image')
    thumb = models.ImageField(upload_to='thumbs')
