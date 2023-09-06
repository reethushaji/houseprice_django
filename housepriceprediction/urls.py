"""housepriceprediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path
from django.views.generic import TemplateView
from housepriceapp.views import *
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
	re_path(r'^$', index,name='index'),
	re_path(r'^index/$', index,name='index'),
	re_path(r'^login/$', login,name='login'),
	re_path(r'^user_registration/$', user_registration,name='user_registration'),
	re_path(r'^builder_registration/$', builder_registration,name='builder_registration'),
	re_path(r'^user/$', user,name='user'),
	re_path(r'^builder/$', builder,name='builder'),
	re_path(r'^loginac/$', loginac,name='loginac'),
	re_path(r'^userhome/$', userhome,name='userhome'),
	re_path(r'^builderhome/$', builderhome,name='builderhome'),
	re_path(r'^projectdetails/$', projectdetails,name='projectdetails'),
	re_path(r'^projectac/$', projectac,name='projectac'),
	re_path(r'^vqueries/$', vqueries,name='vqueries'),
	re_path(r'^vbuilder/$', vbuilder,name='vbuilder'),
	re_path(r'^adminhome/$', adminhome,name='adminhome'),
	re_path(r'^vuser/$', vuser,name='vuser'),
	re_path(r'^flat_details/$', flat_details,name='flat_details'),
	re_path(r'^flat/$', flat,name='flat'),
	re_path(r'^vbuilder1/$', vbuilder1,name='vbuilder1'),
	re_path(r'^aquery/$', aquery,name='aquery'),
	re_path(r'^que/$', que,name='que'),
	re_path(r'^vproject/$', vproject,name='vproject'),
	re_path(r'^vproject1/$', vproject1,name='vproject1'),
	re_path(r'^delp/$', delp,name='delp'),
	re_path(r'^vflat/$', vflat,name='vflat'),
	re_path(r'^predict/',predict,name='predict'),
	re_path(r'^hpredict/',hpredict,name='hpredict'),
]
