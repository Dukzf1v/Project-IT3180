from django.contrib import admin
from .models import NguoiDung

@admin.register(NguoiDung)
class NguoiDungAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vai_tro')



