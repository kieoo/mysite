"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from learn import views as learn_views


urlpatterns = [
    url(r'^add/$', learn_views.add, name='add'),
    url(r'^$', learn_views.index, name='home'),
    url(r'^add2/(\d+)_and_(\d+)/$', learn_views.add2, name='add2'),
    url(r'^admin/', admin.site.urls),
    url(r'^login_in', learn_views.login),
    url(r'^event_manage/$', learn_views.manage),
    url(r'^accounts/login/$', learn_views.login)
]
