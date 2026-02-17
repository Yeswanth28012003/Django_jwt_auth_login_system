from django.contrib import admin
from .models import SailorUser,Course,Category,Module,video_contents,docs_contents,Video_Activity,Soar_Category,Soar_Quiz_Data,Soar_Quiz_Answer,Soar_Quiz_Average_Score

# Register your models here.
admin.site.register(SailorUser)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(video_contents)
admin.site.register(docs_contents)
admin.site.register(Video_Activity)
admin.site.register(Soar_Category)
admin.site.register(Soar_Quiz_Data)
admin.site.register(Soar_Quiz_Answer)
admin.site.register(Soar_Quiz_Average_Score)


