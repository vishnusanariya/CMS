from . import views
from django.urls import path,include
urlpatterns = [
    path('',views.UploadRefDoc,name='uploadRefDoc' ),
    path('viewRefDoc/',views.view_refDoc ,name='viewRefDoc'),
    path('addRefDoc/',views.addRefdoc ,name='addRefdoc'),
]