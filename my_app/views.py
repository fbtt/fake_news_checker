from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, template_name='base.html')


def new_check(request):

    news_content = request.POST.get('news_content')

    # Consultar modelo e retornar veracidade
    veracidade = 'FALSA'

    stuff_for_frontend = {
        'veracidade': veracidade,
    }

    return render(request, 'my_app/new_check.html', stuff_for_frontend)