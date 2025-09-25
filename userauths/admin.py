from django.contrib import admin
from userauths.models import User,Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','phone']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','gender','country','address']
    search_fields=['full_name','date']
    list_filter=['date']

# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)