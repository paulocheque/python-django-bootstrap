from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from .models import *
from django_smart_autoregister import *


admin.site.site_header = '{{ project_name }} Admin'
admin.site.site_title = '{{ project_name }} Admin'
admin.site.index_title = ''


class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

admin.site.unregister(User)
admin.site.register(User, UserModelAdmin)
# admin.site.register(ApiKey)
admin.site.register(ApiAccess)


auto_configure_admin_for_model(ApiKey, override=True)
auto_configure_admin(['{{ project_name }}_api', 'django_cas'])
