from django.contrib import admin

from msg.models import Msg, MsgSession

admin.site.register(Msg)
admin.site.register(MsgSession)
