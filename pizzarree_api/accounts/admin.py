from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.sessions.models import Session
admin.site.site_header = "Pizzarree Admin"
admin.site.site_title = "Pizzarree Admin Portal"
admin.site.index_title = "Welcome to Pizzarree Shop Portal"
admin.site.register(User, UserAdmin)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)
