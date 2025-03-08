from django.db import models

# Create your models here.
class ChatModel(models.Model):
    system_dialogue = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
class CharaimageModel(models.Model):
    charaimage = models.ImageField(upload_to='images/')