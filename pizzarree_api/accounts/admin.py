import pprint

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.sessions.models import Session
admin.site.site_header = "Pizzarree Admin"
admin.site.site_title = "Pizzarree Admin Portal"
admin.site.index_title = "Welcome to Pizzarree Shop Portal"
admin.site.register(User, UserAdmin)
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags = True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
    date_hierarchy = 'expire_date'
