from django.contrib import admin

from users.models import AnnouncementForm, User, VerificationCode


admin.site.register(User)
admin.site.register(VerificationCode)
admin.site.register(AnnouncementForm)
