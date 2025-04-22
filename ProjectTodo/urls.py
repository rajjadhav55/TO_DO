from django.urls import path
from . import views

urlpatterns = [
    path('view_task/', views.view_tasks, name='view'),
    path('add_task/', views.add_task, name='add'),
    path('remove_task/', views.remove_task, name='remove'),
    path('test',views.test,name= 'test' ),
    path('', views.view_tasks), 
    path('update_task/', views.update_task, name='update'),
    path("view_users/", views.view_users, name="view_users"),
    path("user_tasks/", views.user_tasks, name= "user_tasks"),
    path("register_user/", views.register_user, name= "register_user"),
    path("user_login/", views.user_login, name= "user_login"),
    path("logout_user/", views.logout_user, name= "logout_user")
    
]
