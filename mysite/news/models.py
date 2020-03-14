from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class News(models.Model):
    news_source = models.CharField(max_length=500)
    cluster_1 = models.IntegerField(default = 0)
    cluster_2 = models.IntegerField(default = 0)

