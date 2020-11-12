from django import forms
from .models import Organization, Department, User, Profile
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


# Model form for User Registration through admin panel
class UserModelForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # password2 = forms.CharField(
    #     label="Confirm Password",
    #     widget=forms.PasswordInput(attrs={'class': 'form-control'})
    # )

    class Meta:
        model = User
        fields = ('email', 'organization',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'phone': forms.TextInput(attrs={'class': 'form-control'}),
            # 'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'url': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])
    #     user.organization = requ
    #     if commit:
    #         print("it happend")
    #         user.save()
    #     return user


class CustomDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("department_name", "user",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('department_name')

        get_deps = Department.objects.filter(
            department_name=name).filter(user__email=self.request.user)
        # get_organization = OrganizationHead.objects.filter(
        #     department_name=name).filter(organization__email=self.request.user)
        print(self.request.user)
        # get_deps = Department.objects.filter(name=name)
        # get_deps = Department.objects.filter(
        #     organization__email=self.user)

        # get_deps = CustomUser.objects.filter(department__name=name)
        if get_deps.count() != 0:
            raise forms.ValidationError(
                "This department already exists in the organization")


# class ProfileFormSet(BaseInlineFormSet):
#     '''
#     Validate formset data here
#     '''

#     def clean(self):
#         super().clean()

#         percent = 0
#         for form in self.forms:
#             print(form)
#             print(form.cleaned_data["department"])
#             # if form.cleaned_data["department"]
#             raise forms.ValidationError(
#                 _('Total of elements must be 100%%. Current : %(percent).2f%%') % {'percent': percent})

class ProfileFormSet(BaseInlineFormSet):

    def clean(self):
        try:
            for f in self.forms:
                print("Adasda")
                print(f.cleaned_data.get('department'))
                if f.cleaned_data.get('department') is None:
                    raise ValidationError(
                        "One or more required fields is empty")
        except AttributeError:
            pass


class ProfileForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)

    #     self.fields['department'].required = True

    department = forms.ChoiceField(required=True, help_text="Required")

    class Meta:
        model = Profile
        fields = ('address', 'phone', 'department')

    # def clean_department(self):

    #     print('in clean function')
    #     if self.cleaned_data["department"]:
    #         raise forms.ValidationError(
    #             'Please provide EU VAT since you have provided company name.')
    #     # do something that validates your data
    #     return self.cleaned_data["department"]
