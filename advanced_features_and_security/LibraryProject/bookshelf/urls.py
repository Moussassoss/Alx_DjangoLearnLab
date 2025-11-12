from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('example-form/', views.example_form_view, name='example_form_view'),
    path('bookshelf/', include('bookshelf.urls')),
]
