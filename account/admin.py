from django.contrib import admin
from .model import User, Organization
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import User, Organization, Profile, Department
from .forms import UserModelForm, CustomDepartmentForm, ProfileForm, ProfileFormSet

admin.site.register(User)

class ProfileInline(admin.StackedInline):
    model = Profile
    # form = ProfileForm
    formset = ProfileFormSet
    fieldsets = (
        (None, {'fields': ('is_manager', 'address', 'phone', 'department')}),
    )
    # add_fieldsets = (
    #     ('Personal Information', {
    #         'fields': ('organization_email', 'organization_name', 'department', 'is_staff', 'is_active', 'groups',)}
    #      ),
    # )

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('is_manager', 'user')
    fieldsets = (
        (None, {'fields': ('is_manager', 'department',)}),
    )


class UserAdmin(admin.ModelAdmin):
    add_form = UserModelForm
    model = User

    inlines = [
        ProfileInline,
    ]
    list_display = ('email',
                    'is_admin',)
    list_filter = ('is_superuser', 'is_staff',)
    ordering = ('email',)
    filter_horizontal = ()
    search_fields = ('email',)

    fieldsets = (
        ("Information", {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_staff',
                                    'is_active',)}),
    )

    # def get_user(self, obj):
    #     return obj.get_user()

    # def get_fieldsets(self, request, obj=None):
    #     fs = [
    #         ("see",  {'fields': ['address', ]}),
    #         ('Map', {'fields': [],  # required by django admin
    #                  'description':obj.get_user(),
    #                  }),
    #     ]
    #     print(obj.get_user())
    #     return fs

    # def get_fieldsets(self, request, obj=None):
    #     fields = super().get_fields(request, obj)
    #     if obj:
    #         fields_to_remove = []
    #         if request.user.is_superuser:
    #             fields_to_remove = ['is_admin', ]
    #             for field in fields_to_remove:
    #                 fields.remove(field)
    #         return fields

    # def get_fieldsets(self, request, obj=None):
    #     if not request.user.is_admin:
    #         # print("yesss")
    #         print(request.user.password)
    #         fs = [(None, {'fields': ('email', 'title', 'phone', 'description', 'url', 'password', 'is_staff',
    #                                  'is_active', 'is_manager', 'groups',)})]
    #         exclude = ('password2',)
    #         return fs
    #     else:
    #         fs = [(None, {'fields': ('email', 'title', 'phone',
    #                                  'description', 'password')})]

    # return fs

    # def get_fieldsets(self, request, obj=None):
    #     fs = super().get_fieldsets(request, obj)
    #     # fs now contains [(None, {'fields': fields})], do with it whatever you want
    #     fs[0][1]['fields': ('email'), ]
    #     return fs
    # else:
    # return ("Information", {'fields': ('email', 'title', 'phone',
    #    'description', 'password')})

    # /////// yhqn aik function bna k dekho, jo groups field ko replace kr k custom group dy

    add_fieldsets = (
        ('Personal Information', {
            # To create a section with name 'Personal Information' with mentioned fields
            'description': "added_by",
            # To make char fields and text fields of a specific size
            'classes': ('wide',),
            'fields': ('email', 'password1', 'is_staff',
                       'is_active', 'groups',)}
         ),
    )

    readonly_fields = ('is_staff',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # get users related to particular organization to show in the user's list
        related_users = User.objects.filter(
            organization=request.user.organization)
        if request.user.is_superuser:
            return qs
        # elif request.user.is_admin:
        #     return qs
        # print(qs)
        # print(request.user)
        # return qs.filter(id=request.user.id)
        return related_users

    # def has_add_permission(self, request):
    #     if request.user.is_superuser:
    #         return False
    #     return True

# 9/11/2020, rat 9.16 pe isko comment kia tha meny, ku k mjy lgta tha k iski koi zrurt ni
    # def save_model(self, request, obj, form, change):
    #     user = request.user
    #     obj = form.save(commit=False)
    #     # obj.is_admin = True
    #     if obj.email:
    #         obj.added_by = user
    #         obj.save()
    #         form.save_m2m()
    #     return obj

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def save_model(self, request, obj, form, change):
        # if obj.organization:
        #     obj.organization = request.user
        #     obj.save()

        user = request.user
        obj = form.save(commit=False)
        if not change or not obj.user:
            print("in here")
            obj.is_admin = False
            obj.user = user
            obj.organization = request.user.organization
        # instance.modified_by = user
        obj.save()
        # form.save_m2m()
        return obj


class DepartmentAdmin(admin.ModelAdmin):

    form = CustomDepartmentForm
    list_display = ('department_name', 'user')
    list_filter = ('department_name',)
    ordering = ('department_name',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('department_name',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return True

    # def has_view_permission(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return False
    #     return True

    def save_model(self, request, obj, form, change):
        # if obj.organization:
        #     obj.organization = request.user
        #     obj.save()

        user = request.user
        # if user
        obj = form.save(commit=False)
        if not change or not obj.user:
            obj.user = user
        # instance.modified_by = user
        obj.save()
        form.save_m2m()
        return obj

    def get_form(self, request, obj=None, **kwargs):
        DepartmentForm = super().get_form(request, obj, **kwargs)

        class DepartmentFormWithRequest(DepartmentForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return DepartmentForm(*args, **kwargs)
        return DepartmentFormWithRequest


admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Organization)
