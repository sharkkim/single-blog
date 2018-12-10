from django.conf.urls import url
from backweb import views

urlpatterns = [
    # 127.0.0.1:8000/backweb/login/
    url(r'^login/', views.login,name='login'),

    url(r'^register/', views.register,name='register'),

    url(r'^index/',views.index),

    url(r'^article/',views.article,name='article'),

    url(r'^add-article/',views.add_article),

    url(r'^update-article/(\d+)/',views.update_article,name='update-article'),

    url(r'^delete-article/(\d+)/',views.delete_article,name='delete-article'),




]