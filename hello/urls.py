# in this file i specify patterns to route different urls to their appropriate views
# this code contains one route to map root url of the app to the views.home function that was added to hello/views.py

from django.urls import path
from hello import views

urlpatterns = [
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("", views.home, name="home"),
    
    path("login/", views.login, name="login"),
    
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    
    path("user_panel/", views.user_panel, name="user_panel"),
    path("add_image/", views.upload_image, name="add_image"),
    path("logout/", views.login, name="logout"),
    path("create_mask/", views.create_mask, name="create_mask"),
    
    path("upload/", views.upload_image, name="upload_image"),
    
    
    path("select_image_for_binary_mask/", views.select_image_for_binary_mask, name="select_image_for_binary_mask"),
    path("create_binary_mask/<int:image_id>/", views.create_binary_mask, name="create_binary_mask"),
    
    path("save_mask/<int:image_id>/", views.save_mask, name="save_mask"),

    path("view_radiomics_results/", views.view_radiomics_results, name="view_radiomics_results"),
    path("view_radiomics_result/<int:mask_id>/", views.view_radiomics_result, name="view_radiomics_result"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)



