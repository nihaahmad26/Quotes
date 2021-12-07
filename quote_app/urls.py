from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path("quotes", views.show_all),
    path("quotes/page", views.show_page),
    path("quotes/create", views.add_quote),
    path("users/<int:user_id>", views.count),
    path("quotes/<int:quote_id>", views.show_one),
    path("quotes/<int:quote_id>/update", views.update),
    path("quotes/<int:quote_id>/delete", views.delete),
    path("favorite/<int:quote_id>", views.favorite),
    path("unfavorite/<int:quote_id>", views.unfavorite),
    path('logout', views.logout),
    path('success', views.success)
]

