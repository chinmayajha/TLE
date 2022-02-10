from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_app,name='home'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('customer/<str:pk_test>/', views.customer),
	path('resources/', views.resources_page, name='resources'),
	path('dailytask/', views.dailytask_page, name='dailytask'),
	path('leaderboard/',views.leaderboard_page,name='leaderboard'),
    path('logout/',views.logout_page,name='logout'),
    path('contact/',views.contact_page,name='contact'),
	path('team/',views.team_page,name='team'),
	path('allq',views.allq_page,name='allq'),
]
