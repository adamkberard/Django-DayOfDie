from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.players.models import Player


class PlayerAdmin(UserAdmin):
    model = Player
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email', 'username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',
                       'is_staff', 'is_active')}),
    )
    search_fields = ('email', 'username',)
    ordering = ('email', 'username',)


admin.site.register(Player, PlayerAdmin)
