from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class SailorUser(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.PositiveBigIntegerField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10,blank=True,null=True)
    otp_created_at = models.DateTimeField(default=timezone.now)
    is_google_auth =  models.BooleanField(default=False)
    

    def __str__(self):
        return self.name if self.name else self.email.email


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Course(models.Model):
    name =  models.CharField(max_length=100)
    category  = models.ManyToManyField(Category) 
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class  Module(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.name
    
class video_contents(models.Model):
    title = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='video_contents')
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title

class docs_contents(models.Model):
    title = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='docs_contents')
    doc_file = models.FileField(upload_to='docs/')

    def __str__(self):
        return self.title
    
