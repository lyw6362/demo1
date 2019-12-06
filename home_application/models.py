# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class User(models.Model):

    username= models.CharField(max_length=50)
    password= models.CharField(max_length=50)
    place = models.CharField(max_length=20)

    class Meta:
        db_table="t_userInfo"

class ServerInfo(models.Model):
    servername = models.CharField(max_length=50)
    serverip = models.CharField(max_length=50)
    serverpassword = models.CharField(max_length=50)
    # userid = models.ForeignKey(to=User, on_delete=True)

    class Meta:
        db_table= 't_serverInfo'