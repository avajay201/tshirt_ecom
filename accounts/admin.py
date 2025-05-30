from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User
from django import forms
from django.contrib.auth.models import Group, Permission


admin.site.unregister(Group)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'mt-2 border border-base-200 rounded-default dark:border-base-700 group-[.errors]:border-red-600 focus:group-[.errors]:outline-red-600 focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 px-3 py-2 w-full max-w-2xl', 'style': 'height: 200px;'})
    )

@admin.register(User)
class UserAdmin(ModelAdmin):
    fields = ('username', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined', 'groups', 'user_permissions')
    readonly_fields = ('password', )

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    form = GroupForm
