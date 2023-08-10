from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateUserAndSendConfirmCodeView, CurrentUserViewSet,
                    GenerateTokenAndReferralCodeView)

app_name = 'app'

router = DefaultRouter()
router.register(r'users', CurrentUserViewSet, basename='users')

auth_urls = [
    path('signup/', CreateUserAndSendConfirmCodeView.as_view(), name='signup'),
    path('code/', GenerateTokenAndReferralCodeView.as_view(), name='code'),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
