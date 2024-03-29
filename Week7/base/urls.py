from django.conf.urls import url
from django.urls import path, include
from rest_framework import permissions
from base import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.conf.urls.static import static
from base.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Jira API",
        default_version='v1',
        description="Test description"
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,)
)

urlpatterns = [
                  path('login/', obtain_jwt_token),
                  path('register/', views.RegisterUserAPIView.as_view()),
                  path('token/', obtain_jwt_token, name='api_token_auth'),
                  path('token-refresh/', refresh_jwt_token, name='api_token_refresh'),
                  url(r'^help/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

                  # path('blocks/', views.BlockList.as_view()),
                  # path('blocks/<int:pk>/', views.BlockDetail.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
router.register('profiles', ProfileViewSet, base_name='profiles')
router.register('projects', ProjectViewSet, base_name='projects')
router.register('project_members', ProjectMemberViewSet, base_name='project_members')
router.register('blocks', BlockViewSet, base_name='blocks')
router.register('tasks', TaskViewSet, base_name='tasks')
# router.register('documents', DocumentViewSet, base_name='documents')
router.register('comments', CommentViewSet, base_name='comments')

urlpatterns += router.urls
