from django.db import models
# from django.contrib.postgres.fields import ArrayField
# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    inputAudioPath = models.FileField(upload_to='audio/', null=False, verbose_name="", default="test.waf")
    outputSummary = models.TextField(default="")
    outputKeywords = models.TextField(default="")
    outputLinks = models.TextField(default="")


    def __str__(self):
        return str(self.inputAudioPath) + " ID : " + str(self.id)
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('map:show_op', kwargs={'id': self.id})
