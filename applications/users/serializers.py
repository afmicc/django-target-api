from allauth.account.adapter import get_adapter
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer

from applications.users.models import User


class UserSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'gender', 'picture', ]
        read_only_fields = ['email', 'id', ]


class RestAuthLoginSerializer(LoginSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class RestAuthRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=User.Gender.choices, required=True)
    name = serializers.CharField(required=True, max_length=250)

    def get_cleaned_data(self):
        super(RestAuthRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'gender': self.validated_data.get('gender', ''),
            'name': self.validated_data.get('name', ''),
            }

    def custom_signup(self, request, user):
        user.name = self.cleaned_data.get('name')
        user.gender = self.cleaned_data.get('gender')

        adapter = get_adapter()
        adapter.save_user(request, user, self)
