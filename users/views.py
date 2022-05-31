from django.contrib.auth import get_user_model

from authemail.views import Signup
from oauth2_provider.views import TokenView
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.serializers import ChangePasswordSerializer
from users.serializers import CustomUserSerializer
from users.serializers import ReadOnlyUserSerializer


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


class UpdateUserView(UpdateAPIView):
    """
    View for user change password.
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        """
        Handle password change of the current user.
        """

        password = request.data.get('password')
        new_password = request.data.get('new_password')

        if None in [password, new_password]:
            return Response(
                data={
                    'error': (
                        f'Required field not found: [password, new_password].'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        current_user_model = self.request.user
        if not current_user_model.check_password(
                serializer.data.get('password')):
            return Response(
                data={'error': 'Wrong password given.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        current_user_model.set_password(
            serializer.data.get('new_password')
        )
        current_user_model.save()
        return Response(
            data={'message': 'Password updated successfully'},
            status=status.HTTP_200_OK
        )
