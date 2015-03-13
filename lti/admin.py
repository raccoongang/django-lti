from django.contrib import admin

from lti.models import LTIUser


class LTIUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_fk')


admin.site.register(LTIUser, LTIUserAdmin)
