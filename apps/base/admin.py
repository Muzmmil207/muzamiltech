from django.contrib import admin

from .models import Contact, NewsletterSubscriber

admin.site.register(NewsletterSubscriber)
admin.site.register(Contact)
