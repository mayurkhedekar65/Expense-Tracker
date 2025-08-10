from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="anyindex"),
        path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
]

