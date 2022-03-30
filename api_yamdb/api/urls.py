from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

#router = routers.DefaultRouter()
#router.register(r'titles/(?P<title_id>\d+)/reviews',
                #ReviewsViewSet, basename='reviews')





urlpatterns = [
    # path('v1/', include(router.urls))
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]