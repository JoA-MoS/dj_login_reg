from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^combined/', views.disp_login_reg, name='disp_reg_login'),
    url(r'^register/', views.disp_reg, name='disp_reg'),
    url(r'^users/new/', views.register, name='create_user'),
    url(r'^login/$', views.disp_login, name='disp_login'),
    url(r'^login/process/$', views.login, name='do_login'),
    url(r'^logout/$', views.logout, name='do_logout'),
    url(r'^users/list/$', views.disp_users, name='disp_users'),

]
