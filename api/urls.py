from django.urls import include, path

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),

    path('targets/', include('applications.targets.urls')),
    path('contacts/', include('applications.contacts.urls')),
    path('chats/', include('applications.chats.urls')),
]
