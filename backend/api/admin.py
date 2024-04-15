from django.contrib import admin
from .models import *
from django.contrib import admin

admin.site.register(Listing)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'class_year', 'phone_number', 'create_date', 'update_date')
    search_fields = ('username', 'email')
    readonly_fields = ('id', 'create_date', 'update_date')

admin.site.register(User, UserAdmin)
admin.site.register(Image)
admin.site.register(Transaction)
admin.site.register(MyBids)
