from django.contrib import admin

# Register your models here.
from .models import Tweets,Profile

class TweetAdmin(admin.ModelAdmin):
    list_display = ['__str__','user']
    search_fields = ['user__username','user__email','content']
    class Meta:
        model = Tweets


admin.site.register(Tweets,TweetAdmin)
admin.site.register(Profile)
