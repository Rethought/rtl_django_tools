from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from rtl_django_tools.models import User
from rtl_django_tools.forms import BasicUserChangeForm
from rtl_django_tools.forms import BasicUserCreationForm


class BasicUserAdmin(UserAdmin):
    """
    Administer the no-username user instances. A slight modification of
    Django's own UserAdmin given that all we do is remove the username.
    """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    form = BasicUserChangeForm
    add_form = BasicUserCreationForm


admin.site.register(User, BasicUserAdmin)
