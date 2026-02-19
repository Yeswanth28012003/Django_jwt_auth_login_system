from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
class BaseModel(models.Model):
    is_deleted = models.BooleanField(default = False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    objects = models.Manager() 
    active_objects = SoftDeleteManager()  

    class Meta:
        abstract = True
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()
        










class SailorUser(BaseModel):
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    Gender = models.CharField(max_length=100,blank=True,null=True)
    Date_of_birth = models.DateField(blank=True,null=True)
    company = models.CharField(max_length=100,blank=True,null= True)
    age = models.IntegerField(blank=True, null=True)
    work  = models.CharField(max_length=100,blank=True,null=True)
    rank = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.PositiveBigIntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10,blank=True,null=True)
    otp_created_at = models.DateTimeField(default=timezone.now)
    is_google_auth =  models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True,
        blank=True)
    is_verified = models.BooleanField(default=False)
 

    
    

    def __str__(self):
        return self.name if self.name else self.email.email


class Category(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Course(BaseModel):
    name =  models.CharField(max_length=100)
    category  = models.ManyToManyField(Category) 
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class  Module(BaseModel):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.name
    
class video_contents(BaseModel):
    title = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='video_contents')
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title

class docs_contents(BaseModel):
    title = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='docs_contents')
    doc_file = models.FileField(upload_to='docs/')

    def __str__(self):
        return self.title
    
class Video_Activity(BaseModel):
    video = models.ForeignKey(
        'video_contents',
        on_delete=models.CASCADE, 
        related_name='activities'
    )
    activity_time = models.TimeField() 
    type = models.CharField(max_length=50)
    
class Soar_Category(BaseModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Soar_Quiz_Data(BaseModel):
    category = models.ForeignKey(Soar_Category, on_delete = models.CASCADE, related_name='Soar_Analysis')
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    option_e = models.CharField(max_length=255)
    
    def __str__(self):
        return self.question + " (" + self.category.name + ")"
    
class  Soar_Quiz_Answer(BaseModel):
    SailorUser = models.ForeignKey(SailorUser, on_delete=models.CASCADE, related_name='quiz_answers')
    category = models.ForeignKey(Soar_Category, on_delete=models.CASCADE, related_name='quiz_answers')
    quiz_data = models.ForeignKey(Soar_Quiz_Data, on_delete=models.CASCADE, related_name='answers')
    selected_option = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    attempt= models.IntegerField(default=0)

    


    def __str__(self):
        return f"{self.SailorUser.name}" + " - " + self.category.name + " - " + self.quiz_data.question + " - " + self.selected_option

class Soar_Quiz_Average_Score(BaseModel):
    SailorUser = models.ForeignKey(SailorUser, on_delete=models.CASCADE, related_name='average_scores')
    category = models.ForeignKey(Soar_Category, on_delete=models.CASCADE, related_name='average_scores')
    average_score = models.FloatField()
    attempt = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=timezone.now)
    

    def __str__(self):
        return  self.SailorUser.email.email + str(self.average_score) + str(self.date)


