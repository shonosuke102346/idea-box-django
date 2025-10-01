from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ideas import views # viewsをまとめてインポートするのがシンプルです

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # Function-based views
    path('', views.idea_list, name='idea_list'),
    path('create/', views.idea_create, name='idea_create'),
    path('like/<int:idea_id>/', views.like_idea, name='like_idea'),
    
    # Class-based views
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('idea/<int:pk>/', views.IdeaDetailView.as_view(), name='idea_detail'),
    path('idea/<int:pk>/edit/', views.IdeaUpdateView.as_view(), name='idea_update'),
    path('idea/<int:pk>/delete/', views.IdeaDeleteView.as_view(), name='idea_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)