from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse
from desksolutions.forms import OrganizationForm, RegisterForm, ProfileForm
from account.models import Organization, User
from .decorators import organization_absent
from django.core import serializers
import json

from ProjectDeskSolutions3 import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def home(request):
    return render(request, "desksolutions/base.html")


def OrganizationRegister(request):
    context = {}
    if request.method == "POST" and request.is_ajax():
        print("request is POST")
        form = OrganizationForm(request.POST or None)
        # print(form)
        if form.is_valid():
            print("Organization Form is Valid")

            # org = form.save()
            # print(org)
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            url = form.cleaned_data['url']
            create_organization = Organization.objects.create(
                title=title, description=description, url=url)
            create_organization.save()
            # get_org = Organization.objects.filter(
            #     title=title)
            # print(get_org)

            # for g in get_org:
            #     print(g)
            # print(get_org)
            # ser_instance = serializers.serialize(
            # 'json', get_org)
            # print(ser_instance)
            # ser_instance = json.dumps(get_org, content_type='application/json')
            # print(ser_instance)
            request.session['organization'] = create_organization.id
            # print(ser_instance)
            print(request.session['organization'])
            # form.save()
            # return redirect("signup:signups", args=(request.session['organization'],))
            # return redirect('signups')
            # context['json'] = ser_instance
            # return JsonResponse(context)
        else:
            print("Organization Form is inValid")
            # context['register_form'] = form
            context['register_form'] = form.errors
            return JsonResponse(context)
    else:
        form = OrganizationForm()
        context['register_form'] = form

    return render(request, "desksolutions/base.html", context)


@organization_absent
def signup(request):
    session_name = request.session.get('organization')
    print(session_name)
    if session_name is not None:
        context = {}
        get_organization = Organization.objects.get(id=session_name)
        print(get_organization)
        context['organization_title'] = get_organization.title
        # get_org = get_object_or_404(Organization, title=url)
        print("in signup function")

        if request.method == "POST":
            user_form = RegisterForm(request.POST or None)
            profile_form = ProfileForm(request.POST or None)
            if user_form.is_valid() and profile_form.is_valid():
                print("form valid")
                user = user_form.save(commit=False)
                # email = user_form.cleaned_data.get('email')
                # first_name = user_form.cleaned_data.get('first_name')
                # last_name = user_form.cleaned_data.get('last_name')
                # phone = user_form.cleaned_data.get('phone')
                # address = user_form.cleaned_data.get('address')

                # user = User.objects.create_user(
                #     email=email)
                profile = profile_form.save(commit=False)
                # org = request.session.get('organization')
                # for obj in serializers.deserialize("json", org):
                #     print(obj)
                # print(org)
                # print(user)
                # convert_to_obj = json.loads(org)
                # print(convert_to_obj)
                # print(org.id)
                user.organization = get_organization
                user.save()
                group, created = Group.objects.get_or_create(
                    name=settings.GROUP_ALLOCATE)

                ct = ContentType.objects.get_for_model(Organization)
                if created:
                    permission = Permission.objects.filter(content_type=ct)

                    for perm in permission:
                        group.permissions.add(perm)
                    group.save()
                    user.groups.add(group)
                else:
                    user.groups.add(group)
                profile.user = user
                profile.save()
                del request.session['organization']
                return redirect('/admin/login')
                # print(request.session['organization'])
            else:
                print("invalid form")
                context['user_form'] = user_form
                context['profile_form'] = profile_form
        else:
            user_form = RegisterForm()
            profile_form = ProfileForm()
            context['user_form'] = user_form
            context['profile_form'] = profile_form

        return render(request, 'desksolutions/register.html', context)

        #abc
        if methon == 'GET'
