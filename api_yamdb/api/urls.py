from django.urls import include, path
from rest_framework import routers

from .views import (
    AccessTokenObtainView,
    CategoryViewSet,
    ConfirmationCodeObtainView,
    ReviewViewSet,
    CommentsViewSet,
    UserViewSet,
)


router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router.register('categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        ConfirmationCodeObtainView.as_view(),
        name='get_confirm_code'
    ),
    path(
        'v1/auth/token/',
        AccessTokenObtainView.as_view(),
        name='token_obtain'
    ),
]
