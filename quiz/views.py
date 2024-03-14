from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.db.models.functions import TruncDay
from django.db.models import Count
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
import socket


@login_required(login_url='/login/') 
def homepage(request):

    user = request.user.socialaccount_set.filter(user=request.user)

    quiz_list = Quetions.objects.all().filter(user=request.user)
    using_users = Chart.objects.all().filter(user=request.user)


    all_ansver = 0
    for x in Quetions.objects.all().filter(user=request.user):
        all_ansver += x.quetions_list.all().count()




    data = []

    d = Chart.objects.annotate(day=TruncDay('date')).values('day').annotate(c=Count('id')).filter(user=request.user)

    for exp in d:
        data.append({'date':exp['day']  , 'id':exp['c']})



    return render(request, 'mein/index.html',{'chart':data , 'users':quiz_list,'using_users':using_users,'count_list':all_ansver, 'img':user})


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




@login_required(login_url='/login/') 
def create_quiz(request):
    category = Category.objects.all()


    if request.method == 'POST':
        cat_id = Category.objects.get(id=request.POST.get('category'))
        data = Quetions.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            body=request.POST.get('body'),
            duraction_time=request.POST.get('duraction_time'),
            is_score=request.POST.get('is_score'),
            categorys=cat_id
        )
        print(data.random_url)
        return redirect(f'/quiz_signle/{data.random_url}')




    
    return render(request, 'mein/create.html',{'category':category})


@login_required(login_url='/login/') 
def quiz_single(request,url):
    quiz = Quetions.objects.get(random_url=url)

    check_edit = request.user in quiz.is_edit.all()
    if quiz.user == request.user or request.user.is_superuser or check_edit:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        category = Category.objects.all()

        if request.GET.get('title') != None and request.GET.get('body') != None and request.GET.get('duraction_time') != None and request.GET.get('is_score') != None and request.GET.get('category') != None :
            quiz.title =request.GET.get('title')
            quiz.body =request.GET.get('body')
            quiz.duraction_time =request.GET.get('duraction_time')
            quiz.is_score =request.GET.get('is_score')
            quiz.categorys =Category.objects.get(id=request.GET.get('category'))
            quiz.save()
            return redirect(f'/quiz_signle/{quiz.random_url}')

        

        if is_ajax:
            quiz_lists =list(quiz.quetions_list.all().values())
        

            return JsonResponse({'context': quiz_lists })


        return render(request, 'mein/quiz_detail.html',{'quiz':quiz ,'category':category,'quiz_c':{'True':quiz.result.all().filter(is_status=True) , 'False':quiz.result.all().filter(is_status=False) }})

    else:
        return HttpResponse(f'<center><h3>{request.user} Siz bu sahifaga kira olmaysiz {quiz.user} rexsat bermagan</h3></center>')



def dd(request):
    return render(request, 'mein/index.html')

@login_required(login_url='/login/') 
def add_result(request):
    quiz_id = Quetions.objects.get(id= request.GET.get('quiz_id'))
    is_status = False
    count_list = len(quiz_id.quetions_list.all())
    scored = 100 / count_list * int(request.GET.get('true')) 


    if int(scored) >= quiz_id.is_score:
        is_status=True

    else:
        is_status=False
    Result.objects.create(
        user=request.user,
        quiz=quiz_id,
        true= request.GET.get('true'),
        false= request.GET.get('false'),
        time= request.GET.get('time'),
        using_count= request.GET.get('using_count'),
is_status=is_status    ,    
count_score=int(scored)      

    )
    Chart.objects.create(
        user=quiz_id.user
    )



    quiz_id.using_users.add(request.user)

    return redirect('/')


@login_required(login_url='/login/') 
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
    if is_ajax:
        print(is_ajax)
        return JsonResponse(json, safe=False)
  





    movies  = sorted(quiz.result.all(), key=lambda movie: (-movie.true , movie.time))
    print(movies)
    arr = [
    ]
    xcount=0
    for m in movies:
        xcount+=1
        arr.append([m,xcount])

    # json = Quetions_list.objects.get(random_url=url)
        

    return render(request, 'mein/detail.html', {'data':json, 'id':quiz ,'is_have':is_have , 'is_bor':is_have1, 'filter':arr} )


@login_required(login_url='/login/') 
def is_detail(request,url,url2):


    json = Quetions_list.objects.get(random_url=url2)

    return JsonResponse({ 'data':json.true_ansver})



def quetions_list_remove(request,url):


    json = Quetions_list.objects.get(random_url=url)

    json.delete()
    return HttpResponse('delete')


def quetions_list_update(request,url):
    json = Quetions_list.objects.get(random_url=url)
    json.title = request.GET.get('title')
    json.a = request.GET.get('a')
    json.b = request.GET.get('b')
    json.c = request.GET.get('c')
    json.d = request.GET.get('d')
    json.true_ansver = request.GET.get('true_ansver')
    json.save()
    return redirect(f'/quiz_signle/{json.quetions.random_url}/')

def quetions_list_create(request):
    Quetions_list.objects.create(
        title = request.GET.get('title'),
        a = request.GET.get('a'),
        b = request.GET.get('b'),
        c = request.GET.get('c'),
        d = request.GET.get('d'),
        true_ansver = request.GET.get('true_ansver'),
        quetions = Quetions.objects.get(random_url=request.GET.get('random_url')) ,
    )
    title =request.GET.get('title')
    print(f'\n\n{title}\n\n')
    return HttpResponse('true')

    
    # Quetions_list.objects.create(
    #     # quetions=Quetions.objects.get()
    # )



