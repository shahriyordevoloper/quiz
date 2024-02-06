from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist



def homepage(request):
    quiz = Quetions.objects.all().order_by('id')

    return render(request, 'index.html', {'data':quiz})




def detail(request,url):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    quiz = Quetions.objects.get(random_url=url)
    try:
        is_have = Result.objects.get(user=request.user,quiz=quiz)
        print('bor')
    except ObjectDoesNotExist:
        Result.objects.create(user=request.user,quiz=quiz,time='')
        print('yoq')

        pass


    

    json = quiz.quetions_list.all()

    s = model_to_dict(quiz)

    if is_ajax:
        print(is_ajax)
        return JsonResponse(json, safe=False)
    

    return render(request, 'detail.html', {'data':json} )


def is_detail(request,url,url2):

    # page = int(request.GET.get('page'))
    quiz = Quetions.objects.get(random_url=url)
    result = Result.objects.get()


    json = Quetions_list.objects.get(random_url=url2)

    print(json.true_ansver , request.GET.get('value'))
    


    return HttpResponse('sdhfdgf')

