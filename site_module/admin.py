from django.contrib import admin
from .models import Faq, IndexMessages, ContactMessages, ContactRequest


# Register your models here.


class FaqAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'priority', 'for_group']
    list_editable = ['title', 'description', 'priority', 'for_group']


class IndexMessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority', 'for_group']
    list_editable = ['title', 'priority', 'for_group']


admin.site.register(Faq, FaqAdmin)
admin.site.register(IndexMessages, IndexMessagesAdmin)
admin.site.register(ContactRequest)
admin.site.register(ContactMessages)