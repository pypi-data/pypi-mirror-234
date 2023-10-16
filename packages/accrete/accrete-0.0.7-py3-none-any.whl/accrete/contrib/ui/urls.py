from django.urls import path

from . import views

app_name = 'ui'

urlpatterns = [
    path('formmodal/', views.form_modal, name='form_modal'),
]
