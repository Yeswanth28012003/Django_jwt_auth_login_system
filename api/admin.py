from django.contrib import admin
from .models import SailorUser,Course,Category,Module,video_contents,docs_contents,Video_Activity

# Register your models here.
admin.site.register(SailorUser)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(video_contents)
admin.site.register(docs_contents)
admin.site.register(Video_Activity)
