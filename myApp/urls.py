from django.urls import path
from myApp.views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),

    path('my_projects/', my_projects, name='my_projects'),
    path('view_project/<int:id>/', view_project, name='view_project'),
    path('delete_project/<int:id>/', delete_project, name='delete_project'),
    path('add_project/', add_project, name='add_project'),
    path('update_project/<int:id>/', update_project, name='update_project'),
]
