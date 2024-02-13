from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 



class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)






def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')




def homepage(request):
    quiz = Quetions.objects.all().order_by('id')


    return render(request, 'index.html', {'data':quiz})

def dd(request):
    return render(request, 'mein/index.html')

def add_result(request):
    quiz_id = Quetions.objects.get(id= request.GET.get('quiz_id'))
    Result.objects.create(
        user=request.user,
        quiz=quiz_id,
        true= request.GET.get('true'),
        false= request.GET.get('false'),
        time= request.GET.get('time'),
        using_count= request.GET.get('using_count'),

    )
    quiz_id.using_users.add(request.user)

    return redirect('/')


def detail(request,url):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    is_have = ''
    is_have1=''

    quiz = Quetions.objects.get(random_url=url)
    try:
        is_have1 = Result.objects.get(user=request.user,quiz=quiz)
        is_have = 'bor'
    except ObjectDoesNotExist:

        is_have = 'yoq'

        pass


    

    json = quiz.quetions_list.all()

    s = model_to_dict(quiz)

    if is_ajax:
        print(is_ajax)
        return JsonResponse(json, safe=False)
    

    return render(request, 'detail.html', {'data':json, 'id':quiz ,'is_have':is_have , 'is_bor':is_have1} )


def is_detail(request,url,url2):


    json = Quetions_list.objects.get(random_url=url2)

    return JsonResponse({ 'data':json.true_ansver})


