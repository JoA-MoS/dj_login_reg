# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User
import base64


# Create your views here.
def logged_in(ses):
    print ses
    if 'user_id' in ses:
        try:
            User.objects.get(id=ses['user_id'])
            return True
        except:
            return False
    return False

def index(request):
    """ This is a good sample of how to protect a view """
    if logged_in(request.session):
        #if logged in do the stuff you need to do
        return redirect('users:disp_users')
    else:
        return render(request, 'users/combined.html')

def disp_users(request):
    """ This is a good sample of how to protect a view """
    print 'disp users'
    if logged_in(request.session):
        #if logged in do the stuff you need to do
        context = {'users': User.objects.all()}
        return render(request, 'users/list.html', context)
    else:
        #if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(request.path)
        return redirect(reverse('users:disp_login') + '?next={}'.format(next_pg))


def disp_reg(request):
    return render(request, 'users/register.html')


@require_http_methods(['POST'])
def register(request):
    valid, data = User.objects.add(request.POST)
    if valid:
        request.session['user_id'] = data.id
        return redirect(reverse('users:disp_users'))
    else:
        for i in data:
            messages.add_message(request, messages.ERROR, i.message)
    # can we do this better
    return redirect(reverse('users:disp_reg'))

def disp_login_reg(request):
    return render(request, 'users/combined.html')

def disp_login(request):
    context = {}
    if 'next' in request.GET:
        context['next_pg'] = request.GET['next']
    return render(request, 'users/login.html', context)


@require_http_methods(['POST'])
def login(request):
    """Validates user is email and password, sets session variables"""
    valid, data = User.objects.validateLogin(request.POST)
    if valid:
        request.session['user_id'] = data.id
        print 'valid login'
        next_pg = '/'
        if 'next_pg' in request.POST and len(request.POST['next_pg'])>0:
            print 'process next_pg'
            enc = request.POST['next_pg']
            next_pg = base64.urlsafe_b64decode(enc.encode('ascii'))
        print next_pg
        return redirect(next_pg)
    else:
        for i in data:
            messages.add_message(request, messages.ERROR, i.message)
        #TODO: looses next page if they type the password wrong
        return redirect('users:disp_login')

def logout(request):
    request.session.flush()
    messages.add_message(request, messages.SUCCESS, 'You have been logged out')
    return redirect('users:disp_login')
