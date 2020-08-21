from django.urls import include, path
from dj_rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path(
        r'auth/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),

    path('targets/', include('applications.targets.urls')),
    path('contacts/', include('applications.contacts.urls')),
]
