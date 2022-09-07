from django.contrib import admin
from .models import Tag, Mailing, Client, Message


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass