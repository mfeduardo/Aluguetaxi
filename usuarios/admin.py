from django.contrib import admin

from django.contrib.auth import admin as auth_admin

from .forms import UserCreationForm, UserChangeForm
from .models import Usuario

#admin.site.register(Usuario, auth_admin.UserAdmin)

@admin.register(Usuario)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Usuario
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Campos Personalizados", {"fields": ("telefone","cidade", "uf_nome", "image")}),
    )
