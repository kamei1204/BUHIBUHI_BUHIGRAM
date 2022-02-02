from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
# . カレントディレクトリ(現在の階層)のmodelsをimportすることで、modelsの内容を自由に使えるようになる
from . import models

# djangoダッシュボードにこのまま反映される
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ()}),
        (
            _('Permissions'),
            {
               'fields': (
                  'is_active',
                  'is_staff',
                  'is_superuser',
                 )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password')
        }),
    )
# 各種登録
admin.site.register(models.User, UserAdmin)
# admin.site.register+(引数で)簡単にdjangoのダッシュボードにモデル構造を登録、追記ができる
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Comment)
