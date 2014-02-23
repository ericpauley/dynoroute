from django.contrib import admin
from gyms.models import Gym, Route, Membership
from users.models import User

class MembershipInline(admin.TabularInline):
    model = Membership
    list_display = ('gym', 'user', 'level')

class GymAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('name',)
    inlines = [
        MembershipInline,
    ]

class RouteAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('gym', 'name', 'type', 'setter', 'grade')

admin.site.register(Gym, GymAdmin)
admin.site.register(Route, RouteAdmin)
