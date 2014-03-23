from django.contrib import admin
from gyms.models import Gym, Route, GymFollow
from users.models import User

class FollowerInline(admin.TabularInline):
    model = GymFollow
    list_display = ('gym', 'user', 'date_created')

class GymAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('name',)
    inlines = [
        FollowerInline,
    ]

class RouteAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('gym', 'location', 'type', 'setter', 'grade')

admin.site.register(Gym, GymAdmin)
admin.site.register(Route, RouteAdmin)
