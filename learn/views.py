# Create your views here.
# coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return render(request, 'home.html')


def add(request):
    a = request.GET.get('a', 0)
    b = request.GET.get('b', 0)
    c = int(a) + int(b)
    return HttpResponse(u'my test: %s' % str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    for i in range(100):
        pass
    return HttpResponse(u'my test: %s' % str(c))


def login(request):
    user = request.POST.get('username', '')
    passw = request.POST.get('password', '')
    if user == 'qyke' and passw == '1':
        # return HttpResponse(u'congratulation')
        response = HttpResponseRedirect('/event_manage/')
        # response.set_cookie('user', user, 3600)
        request.session['user'] = user
        return response
    else:
        return render(request, 'home.html', {'error': 'error password FUCK YOU'})


def manage(request):
    # manage_user = request.COOKIES.get('user', '')
    manage_user = request.session.get('user', '')
    return render(request, 'event_manage.html', {'my_word': u'Fuck you also', 'my_user': manage_user})
