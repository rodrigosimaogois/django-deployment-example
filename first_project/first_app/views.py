from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import Topic, WebPage, AccessRecord, User
from first_app import forms
from first_app.forms import NewUserForm, UserForm, UserProfileInfoForm

# login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    context_dict = {'text':'hello world', 'number':100}
    return render(request, "first_app/index.html", context=context_dict)
    # webpages_list = AccessRecord.objects.order_by('date')
    # date_dict = {'access_records': webpages_list}
    # return render(request, 'first_app/index.html', context=date_dict)

@login_required
def special(request):
    return HttpResponse("Super!! you are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def other(request):
    return render(request, "first_app/other.html")

def relative(request):
    return render(request, "first_app/relative_url_templates.html")

def help(request):
    my_dict = {
        'help': "aaaa"
    }
    return render(request, 'first_app/help.html', context=my_dict)

def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            # do something code
            print("validation success!")
            print("name " + form.cleaned_data['name'])
            print("email " + form.cleaned_data['email'])
            print("vemail " + form.cleaned_data['verify_email'])
            print("text " + form.cleaned_data['text'])

    return render(request, 'first_app/form_page.html', {'form': form})

def users_view(request):

   form = NewUserForm()

   if request.method == "POST":
       form = NewUserForm(request.POST)
       if form.is_valid():
            form.save(commit=True)
            return index(request)
       else:
            print("ERROR FORM INVALID")

   return render(request, 'first_app/users.html', {'form': form})

def register(request):

    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'first_app/registration.html', {
                                    'user_form': user_form,
                                    'profile_form': profile_form,
                                    'registered': registered
                                    })


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print(f"Username {username} and password {password}")
            return HttpResponse("Invalid login")

    else:
        return render(request, 'first_app/login.html', {})
