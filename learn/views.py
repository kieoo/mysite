# Create your views here.
# coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from learn.models import Event, Guest
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage


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
    user_auth = auth.authenticate(username=user, password=passw)
    if user_auth is not None:
        auth.login(request, user_auth)  # let the login_required know I have login
        # return HttpResponse(u'congratulation')
        response = HttpResponseRedirect('/event_manage/')
        # response.set_cookie('user', user, 3600)
        request.session['user'] = user
        return response
    else:
        return render(request, 'home.html', {'error': 'error password FUCK YOU'})


@login_required
def manage(request):
    # manage_user = request.COOKIES.get('user', '')
    event_list = Event.objects.all()
    manage_user = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': manage_user,
                                                 'events': event_list})


def search(request, path):
    manage_user = request.session.get('user', '')
    search_con = request.GET.get('search_name', '')
    search_con_bytes = search_con.encode(encoding='utf-8')
    if path == 'event':
        event_list = Event.objects.filter(name__contains=search_con_bytes)
        return render(request, 'event_manage.html', {'user': manage_user,
                                                     'events': event_list})
    elif path == 'guest':
        event_list = Guest.objects.filter(realname__contains=search_con_bytes)
        paginator = Paginator(event_list, 1)
        page = request.GET.get('page')
        try:
            contact = paginator.page(page)
        except PageNotAnInteger:
            contact = paginator.page(1)
        except EmptyPage:
            contact = paginator.page(paginator.num_pages)
        return render(request, 'guest_manage.html', {'user': manage_user,
                                                     'guests': contact})


@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 1)
    page = request.GET.get('page')
    try:
        contact = paginator.page(page)
    except PageNotAnInteger:
        contact = paginator.page(1)
    except EmptyPage:
        contact = paginator.page(paginator.num_pages)
    manage_user = request.session.get('user', '')
    return render(request, 'guest_manage.html', {'user': manage_user,
                                                 'guests': contact})


@login_required
def sign_index(request, event_index):
    event = get_object_or_404(Event, id=event_index)  # 获取数据库中id = event_index的数据，存在即返回信息
    return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_action(request, event_index):
    event = get_object_or_404(Event, id=event_index)
    phone = request.POST.get('phone')
    result = Guest.objects.filter(phone=phone, event_id=event_index)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hit': '该用户 未参加此次发布会'})
    elif result[0].sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hit': '该用户 已签到'})
    else:
        Guest.objects.filter(phone=phone).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'guest': result,
                                                   'hit': '该用户 签到成功'})
