from django.urls import path
from docuploaderapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.Login, name='login'),
    path('register/', views.Register, name ='register'),
    path('home/', login_required(views.Home.as_view()), name='home'),
    path('status/<int:pk>', login_required(views.Doc_Status.as_view()), name='status'),
    path('update/<int:id>', login_required(views.Update), name='update'),
    path('delete/<int:id>', login_required(views.delete_data), name='delete'),
    path('document/', login_required(views.Uploaded_Doc), name='document'),
    path('logout/', views.Logout,name='logout'),
]
 