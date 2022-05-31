from django.contrib.auth import get_user_model

from authemail.views import Signup
from oauth2_provider.views import TokenView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.serializers import CustomUserSerializer, ReadOnlyUserSerializer


class ListUserViewSet(ReadOnlyModelViewSet):
    """
    List all users
    """

    serializer_class = CustomUserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        """
         Override serializer function to handle custom response
         for anonymous API user.
        """

        serializer_class = super().get_serializer_class()
        if not self.request.auth:
            serializer_class = ReadOnlyUserSerializer
        return serializer_class


class LoginUserView(TokenView):
    """
    User Login View
    """

    queryset = get_user_model().objects.filter(
        is_verified=True
    )
    permission_classes = (IsAuthenticated,)


class RegisterUserView(Signup):
    """
    View for user registration.
    """

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
        Function to customize post response of the user registration.
        """

        response = super().post(request, format)
        if response.status_code == status.HTTP_201_CREATED:
            custom_data = {
                    'user': response.data,
                    'errors': None
                }
        else:
            custom_data = {
                    'user': None,
                    'errors': response.data
                }
        response.data = custom_data
        return response
