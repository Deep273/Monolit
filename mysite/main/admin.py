from django.contrib import admin
from .models import Poll, PollOption

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 1  # Добавляем одну строку для создания варианта

class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'start_date', 'end_date', 'is_active']
    inlines = [PollOptionInline]

admin.site.register(Poll, PollAdmin)