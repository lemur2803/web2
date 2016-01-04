"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

urlpatterns = [
    url(r'^index/$', 'home_page.views.index', name='index_page'),
    url(r'^about/$', 'home_page.views.about', name='about_page'),
    url(r'^gallery/$', 'home_page.views.gallery', name='gallery_page'),
    url(r'^signin/$', 'home_page.views.signin', name='signin_page'),
    url(r'^signup/$', 'home_page.views.signup', name='signup_page'),
    url(r'^singout/$', 'home_page.views.signout', name='signout_page'),
    url(r'^users/$', 'home_page.views.users', name='get_users'),
    url(r'^visits/$', 'home_page.views.visits', name='visits_page'),
    url(r'^gallery/get_comments/$', 'home_page.views.get_comments', name='get_comments'),
    url(r'^gallery/send_comment/$', 'home_page.views.send_comment', name='send_comment'),
    url(r'^gallery/delete_comment/(?P<id_comment>[0-9]+)$', 'home_page.views.delete_comment', name='delete_comment'),
    url(r'^gallery/send_like/$', 'home_page.views.send_like', name='send_like'),
    url(r'^gallery/get_likes_count/$', 'home_page.views.get_likes_count', name='get_likes_count'),
    url(r'^comments/(?P<id_image>[0-9]+)$', 'home_page.views.comments', name='get_commentsOut'),
]
